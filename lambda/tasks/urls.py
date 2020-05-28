from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="all-tasks"),
    path("mine/", views.MyTaskListView.as_view(), name="my-tasks"),
    path("active/", views.ActiveTaskListView.as_view(), name="active-tasks"),
    path(
        "my-active/",
        views.MyActiveTaskListView.as_view(),
        name="my-active-tasks",
    ),
    path(
        "completed/",
        views.CompletedTaskListView.as_view(),
        name="completed-tasks",
    ),
    path(
        "my-completed/",
        views.MyCompletedTaskListView.as_view(),
        name="my-completed-tasks",
    ),
    path("create/", views.TaskCreateView.as_view(), name="create-task"),
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
