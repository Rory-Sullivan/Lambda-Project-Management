from django import forms
from django.core.exceptions import ValidationError

from . import models


class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = [
            "name",
            "leader",
            "members",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.request_user = user
        super(TeamForm, self).__init__(*args, **kwargs)

        if not user.profile.is_manager:
            self.fields["leader"].queryset = user.profile.get_connections()
            self.fields["members"].queryset = user.profile.get_connections()

    def clean_members(self):
        data = self.cleaned_data["members"]
        user = self.request_user

        if not user.profile.is_manager:
            connections = user.profile.get_connections()

            for member in data:
                if member not in connections:
                    msg = """You do not have permission to add members that are
                    not part of your connections to a team.
                    """
                    raise ValidationError(msg, code="Forbidden")
        return data

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get("leader")
        members = cleaned_data.get("members")

        # NOTE: it would be preferable to include this check on the model but
        # it is difficult to work with many to many fields before the object has
        # been created.
        if leader and members:
            if leader not in members.all():
                msg = f"""
                    The team leader must be included as a member of the team.
                    Please include {leader} in the members section below.
                """
                self.add_error("leader", msg)
