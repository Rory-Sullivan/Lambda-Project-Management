from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks"),
    path("active/", views.ActiveTaskListView.as_view(), name="tasks-active"),
    path(
        "completed/",
        views.CompletedTaskListView.as_view(),
        name="tasks-completed",
    ),
    path("create/", views.TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path(
        "task/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/<int:pk>/complete/",
        views.TaskCompleteView.as_view(),
        name="task-complete",
    ),
    path(
        "task/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
]
