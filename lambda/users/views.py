from django.shortcuts import render, redirect
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
    success_url = "/users/login/"


class UserDetailView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DetailView,
):
    model = User
    permission_required = "users.view_user"
    template_name = "users/user_detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"

    def test_func(self):
        """Only users who share a team can view eachothers profiles"""

        target_user = self.get_object()
        request_user = self.request.user

        for team in target_user.team_set.all():
            if request_user in team.members.all():
                return True

        return False
