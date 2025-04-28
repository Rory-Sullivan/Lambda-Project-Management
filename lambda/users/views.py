from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, mixins
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, reverse
from django.views import generic

from . import forms
from tasks.models import Task
from projects.models import Project
from teams.models import Team


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    template_name = "users/user_register.html"
    success_message = "You're account was successfully created."

    def get_success_url(self):
        return reverse("dashboard")

    def form_valid(self, form):
        super().form_valid(form)
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return redirect(self.get_success_url())


class UserDetailView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DetailView,
):
    model = User
    template_name = "users/user_detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"

    def test_func(self):
        """Only users who share a team or have manager access can view a profile
        """

        target_user = self.get_object()
        request_user = self.request.user

        if request_user.profile.is_manager:
            return True
        return request_user in target_user.profile.get_connections()


class UserUpdateView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.UpdateView
):
    model = User
    fields = ["first_name", "last_name"]
    template_name = "users/user_update.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])

    def test_func(self):
        return not self.request.user.profile.is_demo_user


class UserDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView
):
    model = User
    template_name = "users/user_confirm_delete.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("home")

    def test_func(self):
        return not self.request.user.profile.is_demo_user


def demo_user_login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=settings.DEMO_USER_USERNAME,
            password=settings.DEMO_USER_PASSWORD,
        )

        if user is not None:
            if user.profile.is_demo_user:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

            else:
                msg = (
                    "The user you have provided is not a demo user. Please "
                    + "set a different demo user in your settings or change "
                    + "the current user to a demo user."
                )
                raise PermissionError(msg)

        messages.error(request, "Username or password not correct.")

    return render(request, template_name="users/login_demo_user.html")


class DashboardView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "users/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["task_list"] = (
            Task.objects.filter(completed=False)
            .filter(assigned_to=self.request.user)
            .order_by("date_due", "-priority_level")[:7]
        )

        context["unassigned_task_list"] = (
            Task.objects.filter(completed=False)
            .filter(team__members__in=[self.request.user])
            .filter(assigned_to=None)
            .order_by("date_due", "-priority_level")[:7]
        )

        context["project_list"] = (
            Project.objects.filter(completed=False)
            .filter(team__members=self.request.user)
            .order_by("date_due")
        )

        context["team_list"] = Team.objects.filter(members=self.request.user)

        return context
