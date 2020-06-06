from django import forms
from django.core.exceptions import ValidationError

from . import models
from base import custom_forms


class TeamForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Team
        fields = [
            "name",
            "leader",
            "members",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.request_user

        if not user.profile.is_manager:
            q = user.profile.get_connections()
            self.fields["leader"].queryset = q
            self.fields["members"].queryset = q

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

        return cleaned_data
