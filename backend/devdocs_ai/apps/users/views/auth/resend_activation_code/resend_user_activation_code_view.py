from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.auth.resend_activation_code.resend_user_activation_code_serializer \
    import ResendUserActivationCodeSerializer

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.user.email.email_service import EmailService
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.cache.rollback.cache_rollback_executor import CacheRollbackExecutorService

from utils.services.transaction.transaction_executor_service import TransactionExecutorService

from utils.services.user.activation_code.cache.attempts_expiration.\
    activation_code_attempts_expiration_cache_setter_service \
    import ActivationCodeAttemptsExpirationCacheSetterService

from utils.services.user.resend_activation_code.cache.resend_activation_code_cache_executor \
    import ResenActivationCodeCacheExecutorService

from utils.general_utils import GeneralUtils


class ResendUserActivationCodeView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = ResendUserActivationCodeSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = serializer.validated_data["user"]

        rollbacks = None

        try:
            _, (rollbacks,) = TransactionExecutorService.run(
                db_ops=lambda: serializer.save(),
                next_ops=[
                    lambda: ResenActivationCodeCacheExecutorService.run(
                        user_id=serializer.instance.id
                    )
                ]
            )

            ActivationCodeAttemptsExpirationCacheSetterService.run(
                user_id=serializer.instance.id
            )

            EmailService().send_email_task_sync(
                email_type="resend_code_activation",
                to_email=serializer.instance.email,
                context=GeneralUtils.build_email_context(
                    user_email=serializer.instance.email,
                    activation_code=serializer.instance.activation_code,
                    activation_url=GeneralUtils.build_frontend_url(
                        path="activate-account"
                    ),
                    warning_message=(
                        "Please don't request multiple activation emails in a short period of "
                        "time, as there's a limit for security reasons."
                    )
                )
            )

            return Response(
                {"message": "Activation code has been sent. Check your email."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            CacheRollbackExecutorService.run(
                instance=serializer.instance,
                rollbacks=rollbacks,
                use_case="resend_activation_code",
            )

            return ExceptionResponseHandlerService.run(exc=e)
