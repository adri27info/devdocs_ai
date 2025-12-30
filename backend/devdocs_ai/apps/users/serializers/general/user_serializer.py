from rest_framework import serializers

from apps.users.models import User
from apps.roles.serializers import RoleSerializer

from utils.services.user.create.user_create_data_builder_service import (
    UserCreateDataBuilderService
)
from utils.validators.user.user_attachment_validator import UserAttachmentValidator
from utils.validators.user.user_password_validator import UserPasswordValidator
from utils.validators.user.create.user_create_validator import UserCreateValidator
from utils.exceptions.db.db_exceptions import DatabaseOperationException


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "attachment",
            "role",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "attachment",
            "created_at",
        ]
        extra_kwargs = {
            'first_name': {
                'error_messages': {
                    'max_length': 'First name cannot exceed 20 characters.',
                    'required': 'First name is required.',
                    'blank': 'First name may not be blank.'
                }
            },
            'last_name': {
                'error_messages': {
                    'max_length': 'Last name cannot exceed 50 characters.',
                    'required': 'Last name is required.',
                    'blank': 'Last name may not be blank.'
                }
            },
            'email': {
                'error_messages': {
                    'required': 'Email is required.',
                    'blank': 'Email may not be blank.'
                }
            },
            'password': {
                'validators': [UserPasswordValidator()],
                'write_only': True,
                'error_messages': {
                    'required': 'Password is required.',
                    'blank': 'Password may not be blank.'
                }
            }
        }

    def validate_attachment(self, value):
        UserAttachmentValidator()(
            files=self.context["request"].FILES
        )

        return value

    def validate(self, data):
        default_plan, user_role = UserCreateValidator().run()

        return UserCreateDataBuilderService.run(
            plan=default_plan,
            role=user_role,
            is_active=self.context.get("is_active", False),
            data=data
        )

    def create(self, validated_data):
        try:
            validated_data.pop("attachment", None)

            user = User.objects.create_user(**validated_data)
            return user
        except Exception:
            raise DatabaseOperationException(
                "User could not be created due to invalid or missing data."
            )


class UserUpdateSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "attachment",
        ]
        extra_kwargs = {
            'first_name': {
                'error_messages': {
                    'max_length': 'First name cannot exceed 20 characters.',
                    'blank': 'First name may not be blank.'
                }
            },
            'last_name': {
                'error_messages': {
                    'max_length': 'Last name cannot exceed 50 characters.',
                    'blank': 'Last name may not be blank.'
                }
            },
        }

    def validate_attachment(self, value):
        UserAttachmentValidator()(
            files=self.context["request"].FILES
        )

        return value

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception:
            raise DatabaseOperationException(
                "User could not be updated."
            )


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Current password is required.',
            'blank': 'Current password may not be blank.'
        },
    )

    new_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'New password is required.',
            'blank': 'New password may not be blank.'
        },
        validators=[UserPasswordValidator()],
    )

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")

        return value

    def update(self, instance, validated_data):
        try:
            instance.set_password(validated_data["new_password"])
            instance.save()

            return instance
        except Exception:
            raise DatabaseOperationException(
                "Password could not be updated."
            )
