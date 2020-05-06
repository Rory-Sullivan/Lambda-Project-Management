from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
