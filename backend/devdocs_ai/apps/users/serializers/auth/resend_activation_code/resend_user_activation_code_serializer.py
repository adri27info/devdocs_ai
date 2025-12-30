from rest_framework import serializers

from apps.users.models import User

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_checker_service \
    import ActivationCodeAttemptsCacheCheckerService

from utils.validators.user.activation.user_activation_validator \
    import UserActivationValidator

from utils.exceptions.db.db_exceptions import DatabaseOperationException
from utils.general_utils import GeneralUtils


class ResendUserActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        UserActivationValidator.run(user=user)

        if (ActivationCodeAttemptsCacheCheckerService.run(
            user_id=user.id
        )):
            raise serializers.ValidationError(
                {
                    "detail": (
                        "The maximum number of activation code attempts has been exceeded. "
                        f"Please contact the admin for assistance via the following link: "
                        f"{GeneralUtils.build_frontend_url(path='assistance')}"
                    )
                }
            )

        data["user"] = user
        return data

    def update(self, instance, validated_data):
        try:
            instance.activation_code = GeneralUtils.generate_activation_code()
            instance.save(update_fields=["activation_code"])

            return instance
        except Exception:
            raise DatabaseOperationException(
                "Activation code could not be updated."
            )
