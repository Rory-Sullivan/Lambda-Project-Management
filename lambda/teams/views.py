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
    """Shows a list of all users teams"""

    model = Team

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)


class TeamDetailView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DetailView,
):
    model = Team

    def test_func(self):
        team = self.get_object()
        return team.has_member(self.request.user)


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
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
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

    def test_func(self):
        team = self.get_object()
        return team.leader_is(self.request.user)


class TeamDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView,
):
    model = Team
    success_url = "/teams"

    def test_func(self):
        team = self.get_object()
        return team.leader_is(self.request.user)