from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from teams.models import Team


class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    team = models.ForeignKey(Team, on_delete=models.PROTECT)

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_projects",
    )  # Set to current user on form validation
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="modified_projects",
    )  # Set to current user on form validation
    date_due = models.DateField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_projects",
    )  # Set to current user on form validation

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})
