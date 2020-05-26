from django.shortcuts import render, redirect
from django.contrib.auth import mixins
from django.views import generic
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Automatically saves our new user.
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"Your account has been created. You are now able to log in",
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


class UserDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/user_detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"
