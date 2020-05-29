from django.shortcuts import render, redirect
from django.contrib.auth import mixins
from django.views import generic
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User, Group

NORMAL_USER_GROUP = Group.objects.get(pk=1)


class UserCreateView(generic.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    template_name = "users/user_register.html"
    success_message = (
        "You're account was successfully created you can now login."
    )
    success_url = "/users/login/"


class UserDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/user_detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"
