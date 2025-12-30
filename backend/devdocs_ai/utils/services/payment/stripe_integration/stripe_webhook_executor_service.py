import requests
import stripe
import imgkit

from django.conf import settings
from django.core.files.base import ContentFile

from apps.invoices.models import Invoice
from apps.users.models import User

from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.services.transaction.transaction_executor_service import TransactionExecutorService
from utils.validators.payment.stripe_integration.stripe_checkout_session_user_validator import (
    StripeCheckoutSessionUserValidator
)


class StripeWebhookExecutor:
    """
    Handles Stripe webhook events by verifying the signature and executing
    the appropriate business logic. Supports processing completed
    checkout sessions for updating user plans and creating invoices.
    """

    __STRIPE_WEBHOOK_SECRET = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)

    def __init__(self, *, payload, sig_header):
        self.payload = payload
        self.sig_header = sig_header
        self.endpoint_secret = self.__STRIPE_WEBHOOK_SECRET
        self.event = None

    def verify_event(self):
        """
        Verify and parse the Stripe webhook event.
        """
        checks = {
            not self.payload: InstanceInvalidValueException,
            not self.sig_header: InstanceInvalidValueException,
            not self.endpoint_secret: InstanceInvalidValueException,
        }

        for condition, exc_class in checks.items():
            if condition:
                raise exc_class()

        self.event = stripe.Webhook.construct_event(
            payload=self.payload,
            sig_header=self.sig_header,
            secret=self.endpoint_secret,
        )
        return self.event

    def execute(self):
        """
        Route event to the proper handler.
        """
        if self.event["type"] == "checkout.session.completed":
            self.handle_checkout_session_completed(
                session=self.event["data"]["object"]
            )

    def handle_checkout_session_completed(self, *, session):
        """
        Process completed checkout session:
        - Capture payment if needed.
        - Fetch invoice or charge receipt URL.
        - Save user plan and invoice.
        """
        payment_intent_id = session.get("payment_intent")

        try:
            if isinstance(payment_intent_id, dict):
                payment_intent_id = payment_intent_id.get("id")
            elif not isinstance(payment_intent_id, str):
                payment_intent_id = None

            user_id = session.get("metadata", {}).get("user_id")
            user = User.objects.filter(pk=user_id).first()

            plan_type = StripeCheckoutSessionUserValidator.run(
                stripe_api_key=None,
                user=user,
                skip_stripe_api_key=True,
            )

            if payment_intent_id:
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                invoice_id = payment_intent.get("invoice")
                html_url = None

                if invoice_id:
                    stripe_invoice = stripe.Invoice.retrieve(invoice_id)
                    html_url = stripe_invoice.invoice_pdf
                else:
                    latest_charge_id = payment_intent.get("latest_charge")
                    if latest_charge_id:
                        charge = stripe.Charge.retrieve(latest_charge_id)
                        html_url = charge.get("receipt_url")

            user.plan_type = plan_type
            invoice = Invoice(
                user=user,
                plan_type=plan_type
            )

            if html_url:
                response = requests.get(html_url, timeout=5)
                response.raise_for_status()
                html_content = response.text

                png_bytes = imgkit.from_string(
                    html_content,
                    False,
                    options={"format": "png"}
                )

                invoice.attachment.save(
                    "invoice.png",
                    ContentFile(png_bytes),
                    save=False
                )

            TransactionExecutorService.run(
                db_ops=lambda: (
                    user.save(),
                    invoice.save(),
                )
            )

            if payment_intent.status == "requires_capture":
                stripe.PaymentIntent.capture(payment_intent_id)

        except Exception as e:
            if payment_intent_id:
                try:
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    if payment_intent.status in [
                        "requires_capture",
                        "requires_payment_method",
                        "requires_action",
                        "processing",
                    ]:
                        stripe.PaymentIntent.cancel(payment_intent_id)
                except Exception as cancel_error:
                    raise cancel_error
            raise e
