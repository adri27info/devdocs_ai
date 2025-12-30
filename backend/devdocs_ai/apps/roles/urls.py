from django.urls import path

from apps.roles.views import RoleView

urlpatterns = [
    path("", RoleView.as_view(), name="roles"),
]
