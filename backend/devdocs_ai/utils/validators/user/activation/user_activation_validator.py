from datetime import datetime

from django.utils import timezone

from rest_framework import serializers

from utils.cache.cache_utils import CacheUtils


class UserActivationValidator:
    """
    Validator to ensure a user can activate their account using an activation code.
    """

    @staticmethod
    def run(*, user, activation_code=None):
        """
        Validates user activation status and code.

        Args:
            user (User): User instance to validate.
            activation_code (str, optional): Activation code provided by the user.

        Raises:
            serializers.ValidationError: If user does not exist, is already active,
                code is invalid, or code has expired.
        """
        if not user:
            raise serializers.ValidationError(
                {
                    "detail": "User with this email does not exist."
                }
            )

        if user.is_active:
            raise serializers.ValidationError(
                {
                    "detail": "This account is already active."
                }
            )

        if activation_code:
            if not user.activation_code or user.activation_code != activation_code:
                raise serializers.ValidationError(
                    {
                        "detail": "Invalid activation code."
                    }
                )

            cache_key = CacheUtils.build_cache_key(
                key="activation_code_expiration",
                value=user.id
            )

            activation_code_expiration = CacheUtils.get_cache(
                key=cache_key
            )

            if isinstance(activation_code_expiration, dict):
                activation_code_expiration = activation_code_expiration.get(
                    "activation_code_expiration"
                )

            if (
                not activation_code_expiration
                or datetime.fromtimestamp(
                    activation_code_expiration,
                    tz=timezone.get_current_timezone()
                ) < timezone.now()
            ):
                raise serializers.ValidationError(
                    {
                        "detail": "Activation code has expired."
                    }
                )
