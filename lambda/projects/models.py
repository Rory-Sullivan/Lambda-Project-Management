from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

DEFAULT_USER_ID = 1


class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # TODO: team_leader
    team = models.ManyToManyField(User)

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_project_set",
        default=DEFAULT_USER_ID,
    )
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="modified_project_set",
        default=DEFAULT_USER_ID,
    )
    date_due = models.DateField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_project_set",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})
