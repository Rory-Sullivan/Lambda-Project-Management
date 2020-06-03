from django import forms
from . import models
from base.widgets import DurationWidget, DateWidget
from datetime import date
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            "title",
            "description",
            "project",
            "priority_level",
            "estimated_duration",
            "date_due",
        ]
        widgets = {
            "estimated_duration": DurationWidget(),
            "date_due": DateWidget(),
        }


class AssignTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ["assigned_to"]


class CompleteTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            "date_completed",
        ]
        widgets = {"date_completed": DateWidget()}
