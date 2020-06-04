from django import forms
from django.core.exceptions import ValidationError
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.request_user = user
        super(ProjectForm, self).__init__(*args, **kwargs)

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


class CompleteProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            "date_completed",
        ]
        widgets = {"date_completed": DateWidget()}
