from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.payments.tasks import process_stripe_webhook

from utils.mixins.auth.auth_mixins import NoAuthMixin
from utils.mixins.permissions.permissions_mixins import AllowAnyPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import ExceptionResponseHandlerService


class StripeWebhookView(
    NoAuthMixin,
    AllowAnyPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    def post(self, request, *args, **kwargs):
        try:
            payload = request.body
            sig_header = request.headers.get('Stripe-Signature')

            process_stripe_webhook.delay(
                payload=payload,
                sig_header=sig_header
            )

            return Response(
                {
                    "detail": "Webhook processed successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
