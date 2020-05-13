from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path(
        "active/", views.ActiveProjectListView.as_view(), name="projects-active"
    ),
    path(
        "completed/",
        views.CompletedProjectListView.as_view(),
        name="projects-completed",
    ),
    path("create/", views.ProjectCreateView.as_view(), name="project-create"),
    path(
        "project/<int:pk>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "project/<int:pk>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "project/<int:pk>/complete/",
        views.ProjectCompleteView.as_view(),
        name="project-complete",
    ),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project-delete",
    ),
]
