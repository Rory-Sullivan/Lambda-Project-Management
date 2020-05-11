from django.shortcuts import render
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Task
from datetime import date

TASK_FIELDS = [
    "title",
    "description",
    "assigned_to_project",
    "assigned_to_user",
    "priority_level",
    "estimated_duration",
    "date_due",
]


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Task


class TaskDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    model = Task
    fields = TASK_FIELDS
    success_message = "Task #%(id) was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class TaskUpdateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Task
    fields = TASK_FIELDS
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

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)


class TaskDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = "/tasks"
