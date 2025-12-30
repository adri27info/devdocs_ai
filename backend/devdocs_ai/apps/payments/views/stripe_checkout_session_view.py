from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.payments.mixin import PaymentAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import ExceptionResponseHandlerService

from utils.services.payment.stripe_integration.stripe_checkout_session_user_setter_service \
    import StripeCheckoutSessionUserSetterService


class StripeCheckoutSessionView(
    CookieJWTAuthMixin,
    PaymentAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    @validate_refresh_token(revoke=False)
    def post(self, request, *args, **kwargs):
        try:
            session = StripeCheckoutSessionUserSetterService().run(
                user=request.user
            )

            return Response(
                {
                    "message": "Payment session created successfully.",
                    "checkout_url": session.url
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
