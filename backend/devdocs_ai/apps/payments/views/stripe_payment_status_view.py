import stripe

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.payments.serializers import StripePaymentStatusSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.payments.mixin import PaymentAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import ExceptionResponseHandlerService
from utils.services.instace.instance_checker_service import InstanceCheckerService
from utils.services.payment.stripe_integration.stripe_checkout_session_user_executor_service \
    import StripeCheckoutSessionUserExecutorService


class StripePaymentStatusView(
    CookieJWTAuthMixin,
    PaymentAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = StripePaymentStatusSerializer

    @validate_refresh_token(revoke=False)
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data["session_id"]

        try:
            stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)

            InstanceCheckerService.run(
                instance=stripe.api_key,
                message="Stripe Api key is invalid."
            )

            session = stripe.checkout.Session.retrieve(session_id)

            StripeCheckoutSessionUserExecutorService.run(
                session_metadata=session.metadata,
                user_id=request.user.id
            )

            payment_intent_id = session.get("payment_intent")

            if payment_intent_id:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                return Response(
                    {
                        "payment_status": payment_intent.status,
                        "message": "Payment status proccesed successfully."
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "payment_status": "canceled",
                        "message": "Payment status proccesed successfully."
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
