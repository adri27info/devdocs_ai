from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import RefreshPermissionMixin

from utils.services.user.tokens.cookie.cookie_builder_service import (
    CookieBuilderService
)
from utils.services.user.tokens.refresh_token.outstanding.\
    refresh_token_outstanding_setter_service \
    import RefreshTokenOutstandingSetterService

from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class RefreshTokenCustomUserView(
    NoAuthMixin,
    RefreshPermissionMixin,
    APIView
):
    @validate_refresh_token()
    def post(self, request, *args, **kwargs):
        try:
            user = request.refresh_token_user

            response = Response(
                {"message": "Tokens successfully generated."},
                status=status.HTTP_200_OK
            )

            cookie_builder = CookieBuilderService(
                include_access=True,
                include_refresh=True,
                include_csrf=False,
            )
            response_with_cookies, cookies = cookie_builder.run(
                response=response,
                request=request,
                user=user
            )
            RefreshTokenOutstandingSetterService.run(
                refresh_token_str=cookies["refreshtoken"]["value"]
            )

            return response_with_cookies
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
