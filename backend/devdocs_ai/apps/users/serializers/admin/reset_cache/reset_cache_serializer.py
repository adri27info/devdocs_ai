from rest_framework import serializers

from apps.notifications.models import Notification
from apps.users.models import User

from utils.exceptions.db.db_exceptions import DatabaseOperationException
from utils.services.user.admin.admin_reset_cache_executor_service \
    import AdminResetCacheExecutorService


class ResetCacheSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email may not be blank.'
        }
    )

    class Meta:
        model = Notification
        fields = [
            'email',
            'reset_reason'
        ]
        extra_kwargs = {
            'reset_reason': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'Reset reason is required.',
                    'invalid_choice': (
                        "Invalid reset reason. Must be one of: "
                        "'reset_activation_code_attempts' or 'reset_password_attempts'."
                    )
                }
            }
        }

    def create(self, validated_data):
        try:
            request_user = self.context['request'].user
            receiver = User.objects.filter(email=validated_data["email"]).first()

            return AdminResetCacheExecutorService.run(
                validated_data=validated_data,
                request_user=request_user,
                receiver=receiver
            )
        except Exception:
            raise DatabaseOperationException(
                "User cannot add to the project."
            )
