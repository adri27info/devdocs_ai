from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.login.login_user_serializer import (
    LoginUserSerializer
)
from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.user.tokens.cookie.cookie_builder_service import (
    CookieBuilderService
)
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class LoginUserView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data["user"]
            remember_me = serializer.validated_data.get("remember_me", False)

            response = Response(
                {
                    "message": "Logged in successfully.",
                    "user": {
                        "role": {
                            "id": user.role.id,
                            "name": user.role.name
                        }
                    }
                },
                status=status.HTTP_200_OK
            )

            cookie_builder = CookieBuilderService(
                remember_me=remember_me,
            )

            response_with_cookies, _ = cookie_builder.run(
                response=response,
                request=request,
                user=user,
            )

            return response_with_cookies
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
