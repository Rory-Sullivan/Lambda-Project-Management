from django import forms
from django.core.exceptions import ValidationError

from base import custom_forms
from base.widgets import DateWidget

from . import models


class ProjectForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Project
        fields = [
            "name",
            "description",
            "team",
            "date_due",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "off"}),
            "description": forms.Textarea(attrs={"autocomplete": "off"}),
            "date_due": DateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.request_user

        if not user.profile.is_manager:
            q1 = user.team_set.all()
            q2 = user.created_teams.all()
            q = q1 | q2
            self.fields["team"].queryset = q.distinct()

    def clean_team(self):
        team = self.cleaned_data["team"]
        user = self.request_user

        if not user.profile.is_manager:
            user_teams = user.team_set.all().union(user.created_teams.all())

            if team not in user_teams.all():
                msg = """You do not have permission to assign a project to a
                team that you are not a part of.
                """
                raise ValidationError(msg, code="Forbidden")
        return team


class CompleteProjectForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Project
        fields = [
            "date_completed",
        ]
        widgets = {"date_completed": DateWidget()}
