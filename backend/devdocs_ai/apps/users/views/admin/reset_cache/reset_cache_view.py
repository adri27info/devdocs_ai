from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.users.serializers.admin.reset_cache.reset_cache_serializer import ResetCacheSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.mixins.permissions.users.admin.mixin import AdminAuthPermissionMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ResetCacheView(
    CookieJWTAuthMixin,
    AdminAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = ResetCacheSerializer

    @validate_refresh_token(revoke=False)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            EmailService().send_email_task_async(
                email_type="attempts_resolved",
                to_email=serializer.validated_data["email"],
                context=GeneralUtils.build_email_context(
                    user_email=serializer.validated_data["email"],
                    notifications_url=GeneralUtils.build_frontend_url(
                        path="notifications/information"
                    ),
                )
            )

            return Response(
                {
                    "message": "Cache key reset successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
