from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers.general.user_serializer import (
    UserCreateSerializer
)
from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import FlexibleParserMixin

from utils.services.cache.rollback.cache_rollback_executor import CacheRollbackExecutorService
from utils.services.transaction.transaction_executor_service import TransactionExecutorService
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_executor_service \
    import ActivationCodeExpirationCacheExecutorService


class RegisterUserView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    FlexibleParserMixin,
    GenericAPIView
):
    serializer_class = UserCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["is_active"] = False
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = None

        rollback = None

        try:
            _, (rollback,) = TransactionExecutorService.run(
                db_ops=lambda: setattr(serializer, 'instance', serializer.save()),
                next_ops=[
                    lambda: ActivationCodeExpirationCacheExecutorService().run(
                        user_id=serializer.instance.id
                    )
                ]
            )

            uploaded_file = request.FILES.get("attachment")

            if uploaded_file:
                serializer.instance.attachment.save(
                    uploaded_file.name,
                    uploaded_file,
                    save=True
                )

            return Response(
                {
                    "message": "User registered. Check your email shortly for activation code.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            CacheRollbackExecutorService.run(
                instance=serializer.instance,
                rollbacks=rollback,
                use_case="register"
            )

            return ExceptionResponseHandlerService.run(exc=e)
