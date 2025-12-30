from django.urls import path

from apps.users_projects.views import UserProjectView

urlpatterns = [
    path("", UserProjectView.as_view(), name="users_projects"),
]
