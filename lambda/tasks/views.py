from django.shortcuts import render
from django.contrib.auth import mixins
from django.views import generic
from .models import Task


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Task
