from django import forms

from . import models


class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = [
            "name",
            "leader",
            "members",
        ]

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get("leader")
        members = cleaned_data.get("members")

        if leader not in members.all():
            msg = f"""
                The team leader must be included as a member of the team.
                Please include {leader} in the members section below.
            """
            self.add_error("leader", msg)
