from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.stats.stats_user_serializer import StatsUserSerializer

from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.permissions_mixins import AuthWithRefreshPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.decorators.methods.methods_decorators import validate_refresh_token


class StatsUserView(
    CookieJWTAuthMixin,
    AuthWithRefreshPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = StatsUserSerializer

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)

        return Response(
            {
                "message": "User stats retrieved successfully.",
                "stats": serializer.data
            },
            status=status.HTTP_200_OK
        )
