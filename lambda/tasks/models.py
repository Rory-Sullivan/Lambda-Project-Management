from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from projects.models import Project
from datetime import date

DEFAULT_USER_ID = 1


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
    estimated_duration = models.DurationField(help_text="hh:mm")

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_task_set",
        default=DEFAULT_USER_ID,
    )
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="modified_task_set",
        default=DEFAULT_USER_ID,
    )
    date_due = models.DateField(help_text="dd/mm/yyyy")

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_task_set",
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    @property
    def days_till_due(self):
        difference = self.date_due - date.today()
        return difference.days
