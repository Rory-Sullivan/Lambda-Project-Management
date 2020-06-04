from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from base.widgets import DateWidget, DurationWidget

from . import models


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.request_user = user
        super(TaskForm, self).__init__(*args, **kwargs)

        if not user.profile.is_manager:
            self.fields[
                "project"
            ].queryset = user.profile.get_related_projects()

    def clean_project(self):
        project = self.cleaned_data["project"]
        user = self.request_user

        if not user.profile.is_manager:
            if user not in project.team.members.all():
                msg = """You do not have permission to assign a task to a
                project that you are not a part of.
                """
                raise ValidationError(msg, code="Forbidden")

        return project


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
