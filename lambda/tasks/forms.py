from django import forms
from . import models
from base.widgets import DurationWidget, DateWidget


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            "title",
            "description",
            "assigned_to_project",
            "assigned_to_user",
            "priority_level",
            "estimated_duration",
            "date_due",
        ]
        widgets = {
            "estimated_duration": DurationWidget(),
            "date_due": DateWidget(),
        }