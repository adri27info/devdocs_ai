from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.users.serializers.general.user_serializer import UserSerializer


class SessionActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(
        source="token.user",
        read_only=True
    )
    created_at = serializers.DateTimeField(
        source="token.created_at",
        format="%Y-%m-%d %H:%M:%S"
    )
    expires_at = serializers.DateTimeField(
        source="token.expires_at",
        format="%Y-%m-%d %H:%M:%S"
    )
    blacklisted_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = BlacklistedToken
        fields = [
            "user",
            "created_at",
            "expires_at",
            "blacklisted_at",
        ]
