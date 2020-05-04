from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        # The model the form should interact with.
        model = User

        # The fields and order the form should display.
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
