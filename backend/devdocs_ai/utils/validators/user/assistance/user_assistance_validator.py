from rest_framework import serializers

from apps.notifications.models import Notification

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_checker_service \
    import ActivationCodeAttemptsCacheCheckerService

from utils.services.user.reset_password.cache.reset_password_attempts_cache_checker_service \
    import ResetPasswordAttemptsCacheCheckerService


class UserAssistanceValidator:
    """
    Validator responsible for validating user assistance requests.

    This validator ensures that a user assistance request is valid before a new
    notification is created. It enforces the following rules:

    1. The sender must exist.
    2. Only one of the following may be provided:
       - reset_reason
       - message_reason
       (not both simultaneously, but at least one is required).
    3. If reset_reason is provided, the user must have reached the maximum
       allowed number of attempts for the corresponding reset type. Attempt
       limits are verified through cache-based checker services.
    4. A new assistance request cannot be created if there is already a pending
       reset-type notification from the admin to the same user.

    These validations prevent unnecessary, premature, or duplicate assistance
    notifications and ensure that admin attention is only requested when
    appropriate.
    """

    @staticmethod
    def run(*, sender, receiver, reset_reason, message_reason):
        """
        Validates the parameters for a user assistance request.

        Args:
            sender (User):
                The user requesting assistance.
            receiver (User):
                The admin user who will receive the assistance notification.
            reset_reason (str | None):
                The reset-related reason for the request. Must match one of
                the allowed enum values when provided.
            message_reason (str | None):
                A custom free-text reason for the request when no reset reason
                is provided.

        Raises:
            serializers.ValidationError:
                If any of the following conditions are met:
                - The sender does not exist.
                - Both reset_reason and message_reason were provided.
                - Neither reset_reason nor message_reason was provided.
                - A reset_reason is provided but the user has not reached the
                  maximum allowed attempts for the specific reset type.
                - There is already a pending reset-type notification from the
                  admin to the user.
        """
        if not sender:
            raise serializers.ValidationError(
                {
                    "detail": "User with this email does not exist."
                }
            )

        if reset_reason and message_reason:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "You cannot send both reset_reason and message_reason "
                        "at the same time."
                    )
                }
            )

        if not reset_reason and not message_reason:
            raise serializers.ValidationError(
                {
                    "detail": "You must provide either a reset_reason or a message_reason."
                }
            )

        if reset_reason:
            if reset_reason == "reset_password_attempts":
                if (not ResetPasswordAttemptsCacheCheckerService.run(user_id=sender.id)):
                    raise serializers.ValidationError(
                        {
                            "detail": "You have not reached the maximum number of "
                            "reset-password attempts required to create a notification."
                        }
                    )
            elif reset_reason == "reset_activation_code_attempts":
                if (not ActivationCodeAttemptsCacheCheckerService.run(user_id=sender.id)):
                    raise serializers.ValidationError(
                        {
                            "detail": "You have not reached the maximum number of "
                            "activation-code attempts required to create a notification."
                        }
                    )
        pending_notifications = Notification.objects.filter(
            sender=sender,
            receiver=receiver,
            type="reset",
        ).exists()

        if pending_notifications:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "You already have a pending assistance request. The admin will "
                        "contact u shortly."
                    )
                }
            )
