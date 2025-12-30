from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.permissions_mixins import AuthWithRefreshPermissionMixin
from utils.services.user.tokens.cookie.cookie_builder_service import (
    CookieBuilderService
)
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class CSRFTokenUserView(
    CookieJWTAuthMixin,
    AuthWithRefreshPermissionMixin,
    APIView
):
    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        try:
            response = Response(
                {"message": "CSRF token refreshed."},
                status=status.HTTP_200_OK
            )

            cookie_builder = CookieBuilderService(
                include_access=False,
                include_refresh=False,
                include_csrf=True,
            )
            response_with_cookie, _ = cookie_builder.run(
                response=response,
                request=request,
                user=request.user
            )

            return response_with_cookie
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
