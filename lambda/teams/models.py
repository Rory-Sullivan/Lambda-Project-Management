from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)

    leader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="leader_of_teams"
    )
    members = models.ManyToManyField(User)

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_teams"
    )  # Set to current user at form validation
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="modified_teams"
    )  # Set to current user at form validation

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team-detail", kwargs={"pk": self.pk})

    # Authorization checks
    def has_member(self, user):
        return user in self.members.all()

    def leader_is(self, user):
        return user == self.leader

    def was_created_by(self, user):
        return user == self.created_by
