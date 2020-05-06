from django.shortcuts import render
from django.contrib.auth import mixins
from django.views import generic
from .models import Task


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Task


class TaskDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["title", "description", "rollover", "user"]


class TaskUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["title", "description", "rollover", "user"]


class TaskDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView
):
    model = Task
    success_url = "/tasks"

    def test_func(self):
        task = self.get_object()

        if self.request.user == task.user:
            return True
        return False
