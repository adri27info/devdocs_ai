from rest_framework import serializers

from apps.notifications.models import Notification
from apps.users.models import User

from utils.enums.choices_enums import NotificationTypeEnum
from utils.exceptions.db.db_exceptions import DatabaseOperationException
from utils.validators.user.assistance.user_assistance_validator import UserAssistanceValidator
from utils.services.user.assistance.user_assistance_executor_service \
    import UserAssistanceExecutorService


class AssistanceUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True,
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )
    type = serializers.ChoiceField(
        choices=[
            NotificationTypeEnum.INFO,
            NotificationTypeEnum.RESET
        ],
        error_messages={
            'required': 'Type is required.',
            'invalid_choice': "Invalid type. Must be either 'info' or 'reset'."
        }
    )
    sender_email = serializers.EmailField(
        source="sender.email",
        read_only=True
    )
    receiver_email = serializers.EmailField(
        source="receiver.email",
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "email",
            "type",
            "reset_reason",
            "message_reason",
            "sender_email",
            "receiver_email",
        ]
        extra_kwargs = {
            'reset_reason': {
                'error_messages': {
                    "invalid_choice": (
                        "Invalid reset reason. Must be one of: "
                        "'reset_activation_code_attempts' or 'reset_password_attempts'."
                    )
                }
            },
            'message_reason': {
                'error_messages': {
                    'max_length': 'Message reason cannot exceed 100 characters.',
                }
            },
        }

    def validate(self, data):
        sender = User.objects.filter(email=data["email"]).first()
        receiver = User.objects.filter(role__name="admin").first()

        reset_reason = data.get("reset_reason", None)
        message_reason = data.get("message_reason", None)

        UserAssistanceValidator.run(
            sender=sender,
            receiver=receiver,
            reset_reason=reset_reason,
            message_reason=message_reason,
        )

        data["receiver"] = receiver
        return data

    def create(self, validated_data):
        try:
            email = validated_data.pop("email")
            sender = User.objects.get(email=email)
            receiver = validated_data["receiver"]

            notification = UserAssistanceExecutorService.run(
                receiver=receiver,
                sender=sender,
                validated_data=validated_data
            )

            return notification
        except Exception as e:
            raise DatabaseOperationException(
                f"Notification could not be created {e}."
            )
