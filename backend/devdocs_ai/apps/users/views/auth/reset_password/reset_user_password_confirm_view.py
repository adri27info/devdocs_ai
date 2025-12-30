from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.auth.reset_password.reset_user_password_confirm_serializer import (
    ResetUserPasswordConfirmSerializer
)

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.cache.rollback.cache_rollback_executor import CacheRollbackExecutorService
from utils.services.user.reset_password.confirm.cache.reset_password_confirm_cache_executor \
    import ResetPasswordConfirmCacheExecutorService

from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)

from utils.services.cache.cache_before_transaction_getter_service import \
    CacheBeforeTransactionGetterService

from utils.services.user.reset_password.cache.reset_password_attempts_cache_reset_service \
    import ResetPasswordAttemptsCacheResetService

from utils.services.transaction.transaction_executor_service import TransactionExecutorService

from utils.general_utils import GeneralUtils
from utils.services.user.email.email_service import EmailService


class ResetUserPasswordConfirmView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = ResetUserPasswordConfirmSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = serializer.validated_data["user"]

        rollback = None

        try:
            pre_transaction_cache_values = CacheBeforeTransactionGetterService.run(
                user_id=serializer.instance.id,
                action="reset_password_related"
            )

            _, (rollback,) = TransactionExecutorService.run(
                db_ops=lambda: serializer.save(),
                next_ops=[
                    lambda: ResetPasswordConfirmCacheExecutorService.run(
                        user_id=serializer.instance.id
                    )
                ]
            )

            ResetPasswordAttemptsCacheResetService.run(
                user_id=serializer.instance.id
            )

            EmailService().send_email_task_async(
                email_type="password_reset_confirm",
                to_email=serializer.instance.email,
                context=GeneralUtils.build_email_context(
                    user_email=serializer.instance.email,
                    login_url=GeneralUtils.build_frontend_url(
                        path="login"
                    ),
                )
            )

            return Response(
                {
                    "message": "Password reset successfully. Email will be sent shortly."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            CacheRollbackExecutorService.run(
                instance=serializer.instance,
                rollbacks=rollback,
                use_case="reset_password_confirm",
                pre_transaction_cache_values=pre_transaction_cache_values
            )

            return ExceptionResponseHandlerService.run(exc=e)
