from django import forms
from . import models


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = models.TaskComment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"cols": 80, "rows": 5})}


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = models.ProjectComment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"cols": 80, "rows": 5})}
