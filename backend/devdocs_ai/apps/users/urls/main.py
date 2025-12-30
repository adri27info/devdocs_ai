from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.users.views.general.user_view import UserViewSet
from apps.users.views.info.info_user_view import InfoUserView
from apps.users.views.stats.stats_user_view import StatsUserView


router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("me/", InfoUserView.as_view(), name="me"),
    path("me/stats/", StatsUserView.as_view(), name="me_stats"),
]

urlpatterns += router.urls
