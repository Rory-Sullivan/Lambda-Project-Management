from django import forms
from . import models


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = models.TaskComment
        fields = ["text"]


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = models.ProjectComment
        fields = ["text"]
