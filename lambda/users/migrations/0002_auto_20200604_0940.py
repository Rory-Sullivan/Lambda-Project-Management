# Generated by Django 3.0.5 on 2020-06-04 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_team_leader',
            new_name='is_manager',
        ),
    ]