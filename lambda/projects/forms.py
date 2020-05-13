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
