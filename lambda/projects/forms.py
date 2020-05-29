from django import forms
from . import models
from base.widgets import DateWidget


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            "name",
            "description",
            "team",
            "date_due",
        ]
        widgets = {
            "date_due": DateWidget(),
        }


class CompleteProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            "date_completed",
        ]
        widgets = {"date_completed": DateWidget()}
