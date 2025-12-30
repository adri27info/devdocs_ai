from rest_framework import serializers

from apps.notifications.models import Notification

from utils.cache.cache_utils import CacheUtils

from utils.services.user.reset_password.cache.reset_password_attempts_cache_builder_service \
    import ResetPasswordAttemptsCacheBuilderService

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_builder_service import \
    ActivationCodeAttemptsCacheBuilderService


class AdminResetCacheExecutorService:
    """
    Service to reset a user's cache attempts and create a notification.

    This service handles the business logic when an admin resets either password or
    activation code attempts for a user. It verifies the receiver exists, deletes
    the relevant cache key, generates an appropriate message, and creates a
    Notification instance.
    """

    @staticmethod
    def run(*, validated_data, request_user, receiver):
        """
        Execute the admin reset cache process and create a notification.

        Steps performed:
        1. Verify that the receiver exists; raises ValidationError if not.
        2. Determine the reset type from 'reset_reason'.
        3. Delete the corresponding cache key for the user.
        4. Generate the message_reason for the notification.
        5. Create a Notification object with sender, receiver, type, and message.

        Args:
            validated_data (dict): Serializer data containing 'reset_reason'.
            request_user (User): Admin performing the reset.
            receiver (User): Target user to receive the notification.

        Raises:
            serializers.ValidationError: If the receiver does not exist.

        Returns:
            Notification: The newly created Notification instance.
        """
        if not receiver:
            raise serializers.ValidationError(
                {"detail": "User not found to receive the notification."}
            )

        reset_reason = validated_data.get("reset_reason")

        if reset_reason == "reset_password_attempts":
            message_reason = "Admin reset the attempts of your password successfully."

            cache_key = ResetPasswordAttemptsCacheBuilderService.run(user_id=receiver.id)
            CacheUtils.delete_cache(key=cache_key)
        elif reset_reason == "reset_activation_code_attempts":
            message_reason = "Admin reset the attempts of your activation code successfully."

            cache_key = ActivationCodeAttemptsCacheBuilderService.run(user_id=receiver.id)
            CacheUtils.delete_cache(key=cache_key)

        return Notification.objects.create(
            sender=request_user,
            receiver=receiver,
            type="info",
            message_reason=message_reason
        )
