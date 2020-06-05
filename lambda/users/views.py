from django.shortcuts import render, redirect, reverse
from django.contrib.auth import mixins
from django.views import generic
from . import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    template_name = "users/user_register.html"
    success_message = (
        "You're account was successfully created you can now login."
    )

    def get_success_url(self):
        return reverse("login")


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


class UserUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    template_name = "users/user_update.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])


class UserDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("home")
