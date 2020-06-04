from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
