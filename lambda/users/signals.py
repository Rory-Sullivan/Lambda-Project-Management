from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver

NORMAL_USER_GROUP, created = Group.objects.get_or_create(name="Normal user")

if created:
    add_project_permission = Permission.objects.get(name="Can add project")
    add_task_permission = Permission.objects.get(name="Can add task")
    NORMAL_USER_GROUP.permissions.add(add_project_permission)
    NORMAL_USER_GROUP.permissions.add(add_task_permission)
    NORMAL_USER_GROUP.save()


@receiver(post_save, sender=User)
def post_user_save(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(NORMAL_USER_GROUP)
        instance.save()
