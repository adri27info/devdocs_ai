from rest_framework import serializers

from apps.users.models import User

from utils.validators.user.activation.user_activation_validator \
    import UserActivationValidator

from utils.exceptions.db.db_exceptions import DatabaseOperationException


class ActivateUserAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )
    activation_code = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Activation code is required.',
            'blank': 'Activation code may not be blank.'
        }
    )

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        UserActivationValidator.run(
            user=user,
            activation_code=data["activation_code"]
        )

        data["user"] = user
        return data

    def update(self, instance, validated_data):
        try:
            instance.is_active = True
            instance.save(update_fields=["is_active"])

            return instance
        except Exception:
            raise DatabaseOperationException(
                "The activation of the user could not be updated."
            )
