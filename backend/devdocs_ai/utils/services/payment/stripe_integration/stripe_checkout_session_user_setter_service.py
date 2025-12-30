import stripe

from django.conf import settings

from utils.validators.payment.stripe_integration.stripe_checkout_session_user_validator \
    import StripeCheckoutSessionUserValidator


class StripeCheckoutSessionUserSetterService:
    """
    Service to create a Stripe Checkout session for a user. Configured with
    manual capture and metadata to track the user. Ensures validation before
    creating the session.
    """

    __STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", None)
    __STRIPE_PRICE_ID = getattr(settings, "STRIPE_PRICE_ID", None)

    def run(self, *, user):
        """
        Create and return a Stripe Checkout session for a given user.

        Validates the user and environment before creating the session. Attaches
        metadata and configures success/cancel URLs for frontend redirection.

        Args:
            user (User): Django user initiating the checkout.

        Returns:
            stripe.checkout.Session: Created Stripe checkout session object.

        Raises:
            Exception: Propagates any Stripe API or validation exceptions.
        """
        stripe.api_key = self.__STRIPE_SECRET_KEY

        try:
            StripeCheckoutSessionUserValidator.run(
                stripe_api_key=stripe.api_key,
                user=user
            )

            session = stripe.checkout.Session.create(
                mode="payment",
                customer_email=user.email,
                line_items=[{
                    "price": self.__STRIPE_PRICE_ID,
                    "quantity": 1,
                }],
                payment_intent_data={
                    "capture_method": "manual",
                    "metadata": {"user_id": str(user.id)},
                },
                success_url=(
                    f"{settings.FRONTEND_URL}/dashboard/checkout/"
                    f"?session_id={{CHECKOUT_SESSION_ID}}"
                ),
                cancel_url=(
                    f"{settings.FRONTEND_URL}/dashboard/checkout/"
                    f"?session_id={{CHECKOUT_SESSION_ID}}"
                ),
                metadata={"user_id": str(user.id)},
            )

            return session
        except Exception as e:
            raise e
