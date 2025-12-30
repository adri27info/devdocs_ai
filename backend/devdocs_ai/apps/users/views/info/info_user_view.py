from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.permissions_mixins import AuthWithRefreshPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin


class InfoUserView(
    CookieJWTAuthMixin,
    AuthWithRefreshPermissionMixin,
    JSONParserMixin,
    APIView
):
    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "message": "User id retrieved successfully.",
                "user": {
                    "id": request.user.id
                }
            },
            status=status.HTTP_200_OK
        )
