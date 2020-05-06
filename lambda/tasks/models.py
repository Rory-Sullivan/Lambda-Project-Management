from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rollover = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})
