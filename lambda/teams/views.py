from datetime import date

from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views import View, generic

from comments import forms as comment_forms
from comments import views as comment_views

from . import forms
from .models import Team


class TeamListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all teams"""

    model = Team


class MyTeamListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all users teams"""

    model = Team

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)


class TeamDetailView(
    mixins.LoginRequiredMixin, generic.DetailView,
):
    model = Team


class TeamCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView,
):
    model = Team
    form_class = forms.TeamForm
    success_message = "Team {name} was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=cleaned_data.get("name"))

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class TeamUpdateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView,
):
    model = Team
    form_class = forms.TeamForm
    success_message = "Team {name} was updated successfully"

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.success_message.format(name=cleaned_data.get("name"))

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class TeamDeleteView(
    mixins.LoginRequiredMixin, generic.DeleteView,
):
    model = Team
    success_url = "/teams"
