from django.shortcuts import render
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Task
from datetime import date
from . import forms


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all tasks"""

    model = Task


class ActiveTaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of active tasks"""

    model = Task

    def get_queryset(self):
        return Task.objects.filter(completed=False)


class CompletedTaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of active tasks"""

    model = Task

    def get_queryset(self):
        return Task.objects.filter(completed=True)


class TaskDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    model = Task
    form_class = forms.TaskForm
    success_message = "Task #%(id)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class TaskUpdateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Task
    form_class = forms.TaskForm
    success_message = "Task #%(id)s was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class TaskCompleteView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Task
    fields = [
        "completed",
        "date_completed",
    ]
    initial = {
        "completed": True,
        "date_completed": date.today(),
    }
    success_message = "Task #%(id)s completed"
    success_url = "/tasks"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class TaskDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = "/tasks"
