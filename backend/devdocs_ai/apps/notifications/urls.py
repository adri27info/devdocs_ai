from django.urls import path

from apps.notifications.views import (
    NotificationListView,
    NotificationDeleteView
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("<int:pk>/", NotificationDeleteView.as_view(), name="notifications-delete"),
]
