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
    """Shows a list of all projects"""

    model = Project


class MyProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all users projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team=self.request.user)


class ActiveProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of active projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(completed=False)


class MyActiveProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users active projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team=self.request.user).filter(
            completed=False
        )


class CompletedProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of completed projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(completed=True)


class MyCompletedProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users completed projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team=self.request.user).filter(
            completed=True
        )


class ProjectDetailView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.detail.SingleObjectMixin,
    View,
):
    permission_required = "projects.view_project"
    model = Project

    def has_permission(self):
        if super().has_permission():
            return True
        obj = self.get_object()
        user = self.request.user
        if obj.team.filter(pk=user.pk):
            return True
        return False

    def get(self, request, *args, **kwargs):
        view = ProjectDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = comment_views.PostProjectComment.as_view()
        return view(request, *args, **kwargs)


class ProjectDetailDisplay(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = comment_forms.ProjectCommentForm()
        return context


class ProjectCreateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    permission_required = "projects.add_project"
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was created successfully"

    def has_permission(self):
        if super().has_permission():
            return True
        obj = self.get_object()
        user = self.request.user
        if obj.team.filter(pk=user.pk):
            return True
        return False

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    permission_required = "projects.change_project"
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was updated successfully"

    def has_permission(self):
        if super().has_permission():
            return True
        obj = self.get_object()
        user = self.request.user
        if obj.team.filter(pk=user.pk):
            return True
        return False

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ProjectCompleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    permission_required = "projects.change_project"
    model = Project
    form_class = forms.CompleteProjectForm
    initial = {
        "date_completed": date.today(),
    }
    success_message = "Project #%(id)s completed"
    success_url = "/projects"

    def has_permission(self):
        if super().has_permission():
            return True
        obj = self.get_object()
        user = self.request.user
        if obj.team.filter(pk=user.pk):
            return True
        return False

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.DeleteView,
):
    permission_required = "projects.delete_project"
    model = Project
    success_url = "/projects"

    def has_permission(self):
        if super().has_permission():
            return True
        obj = self.get_object()
        user = self.request.user
        if obj.team.filter(pk=user.pk):
            return True
        return False
