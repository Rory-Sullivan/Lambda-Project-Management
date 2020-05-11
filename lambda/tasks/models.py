from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from projects.models import Project


class Task(models.Model):
    PRIORITY_LEVELS = [
        (3, "Low"),
        (6, "Medium"),
        (9, "High"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to_project = models.ForeignKey(Project, on_delete=models.PROTECT)
    assigned_to_user = models.ForeignKey(User, on_delete=models.PROTECT)
    priority_level = models.IntegerField(choices=PRIORITY_LEVELS, default=3)
    estimated_duration = models.DurationField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_due = models.DateField()

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})
