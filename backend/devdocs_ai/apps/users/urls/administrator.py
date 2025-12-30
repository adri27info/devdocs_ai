from django.urls import path

from apps.users.views.admin.reset_cache.reset_cache_view import ResetCacheView
from apps.users.views.admin.session_activity.session_activity_view import SessionActivityView

urlpatterns = [
    path("reset-cache/", ResetCacheView.as_view(), name="reset_cache"),
    path("session-activity/", SessionActivityView.as_view(), name="session_activity"),
]
