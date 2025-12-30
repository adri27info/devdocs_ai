from rest_framework import serializers

from apps.users.models import User

from utils.validators.user.user_validator import UserValidator


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password may not be blank.'
        })
    remember_me = serializers.BooleanField(
        required=False,
        default=False,
        write_only=True,
        error_messages={
            "invalid": "Remember me must be a boolean value."
        }
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        UserValidator.run(user=user, password=password)

        data["user"] = user
        return data
