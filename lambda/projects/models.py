from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # TODO: team_leader
    team = models.ManyToManyField(User)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modifed = models.DateTimeField(auto_now=True)
    date_due = models.DateField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})
