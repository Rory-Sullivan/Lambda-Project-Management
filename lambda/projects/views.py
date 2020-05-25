from django.shortcuts import render
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from comments import forms as comment_forms
from comments import views as comment_views
from .models import Project
from datetime import date
from . import forms


class ProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all projects"""

    model = Project


class ActiveProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of active projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(completed=False)


class CompletedProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of completed projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(completed=True)


class ProjectDetailView(mixins.LoginRequiredMixin, generic.DetailView):
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
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class ProjectUpdateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class ProjectCompleteView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Project
    fields = [
        "completed",
        "date_completed",
    ]
    initial = {
        "completed": True,
        "date_completed": date.today(),
    }
    success_message = "Project #%(id)s completed"
    success_url = "/projects"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class ProjectDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = "/projects"
