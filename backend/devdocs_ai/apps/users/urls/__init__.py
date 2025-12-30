from django.urls import path, include

urlpatterns = [
    path("administrator/", include("apps.users.urls.administrator")),
    path("auth/", include("apps.users.urls.auth")),
    path("users/", include("apps.users.urls.main")),
]
