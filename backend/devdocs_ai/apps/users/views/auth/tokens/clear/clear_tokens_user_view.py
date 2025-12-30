from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import OriginHeaderPermissionMixin
from utils.services.user.tokens.cookie.cookie_cleaner_service import (
    CookieCleanerService
)
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class ClearTokensUserView(
    NoAuthMixin,
    OriginHeaderPermissionMixin,
    APIView
):
    def post(self, request, *args, **kwargs):
        try:
            response = Response(
                {"message": "Authentication cookies cleared."},
                status=status.HTTP_200_OK,
            )
            response = CookieCleanerService.run(
                response=response
            )

            return response
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
