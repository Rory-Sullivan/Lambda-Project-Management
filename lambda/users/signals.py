from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project
from tasks.models import Task
from teams.models import Team

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        team = Team.objects.create(
            name="Just me",
            leader=instance,
            created_by=instance,
            modified_by=instance,
        )
        team.members.set([instance])

        TODO_DESCRIPTION = "Your to do list."
        project = Project.objects.create(
            name="To do",
            description=TODO_DESCRIPTION,
            team=team,
            created_by=instance,
            modified_by=instance,
        )

        TASK_DESCRIPTION = """If you you are seeing this message you have
            obviously already registered for lambda and so you can go ahead and
            complete this task by hitting the button below.
        """
        Task.objects.create(
            title="Register for Lambda",
            description=TASK_DESCRIPTION,
            project=project,
            team=team,
            assigned_to=instance,
            estimated_duration=timedelta(0, 120, 0),
            created_by=instance,
            modified_by=instance,
            date_due=date.today(),
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
