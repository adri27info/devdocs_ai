from rest_framework import serializers

from apps.users.models import User

from utils.general_utils import GeneralUtils
from utils.services.user.reset_password.cache.reset_password_attempts_cache_checker_service \
    import ResetPasswordAttemptsCacheCheckerService

from utils.validators.user.user_validator import UserValidator


class ResetUserPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        UserValidator.run(user=user)

        if (ResetPasswordAttemptsCacheCheckerService.run(
            user_id=user.id
        )):
            raise serializers.ValidationError(
                {
                    "detail": (
                        "The maximum number of reset password attempts has been exceeded. "
                        f"Please contact the admin for assistance via the following link: "
                        f"{GeneralUtils.build_frontend_url(path='assistance')}"
                    )
                }
            )

        data["user"] = user
        return data
