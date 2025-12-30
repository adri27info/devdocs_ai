from django.urls import path

from apps.roles_projects.views import RoleProjectView

urlpatterns = [
    path("", RoleProjectView.as_view(), name="roles_projects"),
]
