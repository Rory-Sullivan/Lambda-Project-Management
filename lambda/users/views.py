from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, "users/login.html")


@login_required
def profile(request):
    return render(request, "users/profile.html")
