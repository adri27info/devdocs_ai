from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.users.serializers.admin.session_activity.session_activity_serializer \
    import SessionActivitySerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.mixins.permissions.users.admin.mixin import AdminAuthPermissionMixin

from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class SessionActivityView(
    CookieJWTAuthMixin,
    AdminAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = SessionActivitySerializer

    def get_queryset(self):
        return BlacklistedToken.objects.select_related("token").all()

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().order_by("-blacklisted_at")
            serializer = self.get_serializer(queryset, many=True)

            return Response(
                {
                    "message": "Session activity retrieved successfully.",
                    "activity": {
                        "list": serializer.data
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
