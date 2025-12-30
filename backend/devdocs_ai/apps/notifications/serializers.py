from rest_framework import serializers

from apps.notifications.models import Notification
from apps.users.serializers.general.user_serializer import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
