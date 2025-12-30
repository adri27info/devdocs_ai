from rest_framework import serializers

from utils.services.user.password.password_reset_token_checker_service import (
    PasswordResetTokenCheckerService
)
from utils.validators.user.user_password_validator import UserPasswordValidator
from utils.validators.user.user_validator import UserValidator
from utils.exceptions.db.db_exceptions import DatabaseOperationException


class ResetUserPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(
        error_messages={
            'required': 'UID is required.',
            'blank': 'UID may not be blank.'
        }
    )
    token = serializers.CharField(
        error_messages={
            'required': 'Token is required.',
            'blank': 'Token may not be blank.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password may not be blank.'
        },
        validators=[UserPasswordValidator()],
    )

    def validate(self, data):
        try:
            user = PasswordResetTokenCheckerService.run(
                uid=data["uid"],
                token=data["token"]
            )
        except Exception:
            raise serializers.ValidationError(
                {
                    "detail": "Invalid uid or user does not exist."
                }
            )

        UserValidator.run(user=user)
        data["user"] = user
        return data

    def update(self, instance, validated_data):
        try:
            instance.set_password(validated_data["password"])
            instance.save()

            return instance
        except Exception:
            raise DatabaseOperationException(
                "Password could not be updated."
            )
