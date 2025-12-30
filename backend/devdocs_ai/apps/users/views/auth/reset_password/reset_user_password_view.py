from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.auth.reset_password.reset_user_password_serializer import (
    ResetUserPasswordSerializer
)

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.cache.rollback.cache_rollback_executor import CacheRollbackExecutorService
from utils.services.user.reset_password.cache.reset_password_attempts_cache_updater_service \
    import ResetPasswordAttemptsCacheUpdaterService

from utils.services.user.password.password_reset_token_builder_service import (
    PasswordResetTokenBuilderService
)
from utils.services.user.email.email_service import EmailService
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.cache.cache_before_transaction_getter_service import \
    CacheBeforeTransactionGetterService

from utils.general_utils import GeneralUtils
from utils.cache.cache_rollback_utils import CacheRollbackUtils


class ResetUserPasswordView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = ResetUserPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = serializer.validated_data["user"]

        rollback = None

        try:
            pre_transaction_cache_values = CacheBeforeTransactionGetterService.run(
                user_id=serializer.instance.id,
                action="reset_password_related"
            )

            rollback = CacheRollbackUtils(
                key="reset_password_attempts",
                user_id=serializer.instance.id
            )
            rollback.backup()

            reset_data = PasswordResetTokenBuilderService.run(
                user=serializer.instance
            )

            ResetPasswordAttemptsCacheUpdaterService.run(
                user_id=serializer.instance.id
            )

            EmailService().send_email_task_sync(
                email_type="password_reset",
                to_email=serializer.instance.email,
                context=GeneralUtils.build_email_context(
                    user_email=serializer.instance.email,
                    password_reset_url=GeneralUtils.build_frontend_url(
                           path=(
                                f"reset-password?"
                                f"uid={reset_data['uid']}&token={reset_data['token']}"
                            )
                    ),
                ),
            )

            return Response(
                {"message": "Password reset link generated. Check your email."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            CacheRollbackExecutorService.run(
                instance=serializer.instance,
                rollbacks=rollback,
                use_case="reset_password",
                pre_transaction_cache_values=pre_transaction_cache_values
            )

            return ExceptionResponseHandlerService.run(exc=e)
