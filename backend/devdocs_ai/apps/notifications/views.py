from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from apps.notifications.filters import NotificationFilter

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.filters.filter_mixins import DjangoBaseFilterMixin
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.notifications.mixin import NotificationAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin


class NotificationListView(
    CookieJWTAuthMixin,
    NotificationAuthPermissionMixin,
    JSONParserMixin,
    DjangoBaseFilterMixin,
    GenericAPIView
):
    filterset_class = NotificationFilter
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "message": "Notifications listed successfully.",
                "notifications": {
                    "list": serializer.data
                }
            },
            status=status.HTTP_200_OK
        )


class NotificationDeleteView(
    CookieJWTAuthMixin,
    NotificationAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    @validate_refresh_token(revoke=False)
    def delete(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.delete()

        return Response(
            {
                "message": "Notification deleted successfully."
            },
            status=status.HTTP_200_OK
        )
