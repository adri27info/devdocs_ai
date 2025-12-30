from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.auth.activate_account.activate_user_account_serializer import (
    ActivateUserAccountSerializer
)

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.user.activation_code.cache.general.activation_code_cache_executor_service \
    import ActivationCodeCacheExecutorService

from utils.services.cache.rollback.cache_rollback_executor import CacheRollbackExecutorService
from utils.services.transaction.transaction_executor_service import TransactionExecutorService
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)

from utils.services.cache.cache_before_transaction_getter_service import \
    CacheBeforeTransactionGetterService

from utils.services.user.activation_code.cache.general.activation_code_cache_reset_service \
    import ActivationCodeCacheResetService


class ActivateUserAccountView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = ActivateUserAccountSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = serializer.validated_data["user"]

        rollbacks = None

        try:
            pre_transaction_cache_values = CacheBeforeTransactionGetterService.run(
                user_id=serializer.instance.id,
                action="activate_account_related"
            )

            _, (rollbacks,) = TransactionExecutorService.run(
                db_ops=lambda: serializer.save(),
                next_ops=[
                    lambda: ActivationCodeCacheExecutorService.run(
                        user_id=serializer.instance.id
                    )
                ]
            )

            ActivationCodeCacheResetService.run(
                user_id=serializer.instance.id
            )

            return Response(
                {"message": "User account successfully activated."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            CacheRollbackExecutorService.run(
                instance=serializer.instance,
                rollbacks=rollbacks,
                use_case="activate_account",
                pre_transaction_cache_values=pre_transaction_cache_values
            )

            return ExceptionResponseHandlerService.run(exc=e)
