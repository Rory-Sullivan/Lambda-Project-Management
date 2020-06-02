from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)

    leader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="leader_of_teams"
    )
    members = models.ManyToManyField(User)

    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_team_set"
    )

    def __str__(self):
        return self.name
