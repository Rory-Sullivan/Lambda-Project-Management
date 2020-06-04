from django.shortcuts import render
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic, View
from comments import forms as comment_forms
from comments import views as comment_views
from .models import Project
from datetime import date
from . import forms


class ProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all users projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user)


class ActiveProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users active projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user).filter(
            completed=False
        )


class CompletedProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users completed projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user).filter(
            completed=True
        )


class ProjectDetailView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic.detail.SingleObjectMixin,
    View,
):
    model = Project

    def get(self, request, *args, **kwargs):
        view = ProjectDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = comment_views.PostProjectComment.as_view()
        return view(request, *args, **kwargs)

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if user.profile.is_manager:
            return True
        if project.was_created_by(user):
            return True
        return project.team_has_member(user)


class ProjectDetailDisplay(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = comment_forms.ProjectCommentForm()
        return context


class ProjectCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView,
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was created successfully"

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was updated successfully"

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if project.was_created_by(user):
            return True
        return project.leader_is(user)


class ProjectCompleteView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Project
    form_class = forms.CompleteProjectForm
    initial = {
        "date_completed": date.today(),
    }
    success_message = "Project #%(id)s completed"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if project.was_created_by(user):
            return True
        return project.leader_is(user)


class ProjectDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView,
):
    model = Project
    success_url = "/projects"

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if project.was_created_by(user):
            return True
        return project.leader_is(user)
