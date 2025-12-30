from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin

from utils.services.user.tokens.cookie.cookie_cleaner_service import (
    CookieCleanerService
)
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class RevokeAndClearTokensUserView(
    CookieJWTAuthMixin,
    AuthWithRefreshAndCSRFPermissionMixin,
    APIView
):
    @validate_refresh_token(require_active=False)
    def post(self, request, *args, **kwargs):
        try:
            response = Response(
                {"message": "Refresh token has been blacklisted."},
                status=status.HTTP_200_OK
            )
            response_without_cookies = CookieCleanerService.run(
                response=response
            )

            return response_without_cookies
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
