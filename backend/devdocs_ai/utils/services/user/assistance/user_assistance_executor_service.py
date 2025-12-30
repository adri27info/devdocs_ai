from rest_framework import serializers

from apps.notifications.models import Notification


class UserAssistanceExecutorService:
    """
    Service responsible for creating user assistance notifications.
    """

    @staticmethod
    def run(*, receiver, sender, validated_data):
        """
        Create a notification for a user assistance request.

        This method validates that a receiver (typically an admin user) exists and then
        creates a Notification instance using the provided sender and validated data.
        If a reset_reason is present, the method automatically generates a
        message_reason based on that value.

        Args:
            receiver (User): The user who will receive the notification.
            sender (User): The user sending the assistance request.
            validated_data (dict): The already validated fields used to create the
                notification. May include reset_reason, message_reason, and other
                Notification fields.

        Returns:
            Notification: The created Notification instance.

        Raises:
            serializers.ValidationError: Raised if no receiver is available to accept
                the notification.
        """
        if not receiver:
            raise serializers.ValidationError(
                {
                    "detail": "No admin user found to receive the notification."
                }
            )

        reset_reason = validated_data.get("reset_reason")

        if reset_reason == "reset_password_attempts":
            validated_data["message_reason"] = (
                "Assistance for reset the password attempts"
            )
        elif reset_reason == "reset_activation_code_attempts":
            validated_data["message_reason"] = (
                "Assistance for reset the activation code attempts"
            )

        return Notification.objects.create(
            sender=sender,
            **validated_data
        )
