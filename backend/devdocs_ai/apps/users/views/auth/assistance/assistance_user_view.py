from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from apps.users.serializers.auth.assistance.assistance_user_serializer import (
    AssistanceUserSerializer
)

from utils.services.user.email.email_service import EmailService
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.general_utils import GeneralUtils


class AssistanceUserView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    CreateAPIView,
):
    serializer_class = AssistanceUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        try:
            EmailService().send_email_task_async(
                email_type="admin_assistance",
                to_email=response.data["receiver_email"],
                context=GeneralUtils.build_email_context(
                    admin_email=response.data["receiver_email"],
                    sender_email=response.data["sender_email"],
                    notification_type=response.data["type"],
                    panel_url=GeneralUtils.build_frontend_url(
                        path="notifications"
                    ),
                )
            )

            return Response(
                {
                    "message": "Notification created successfully. The admin will contact "
                    "you shortly.",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
