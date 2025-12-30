import stripe

from django.conf import settings

from celery import shared_task

from utils.services.payment.stripe_integration.stripe_webhook_executor_service \
    import StripeWebhookExecutor


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_stripe_webhook(self, *, payload, sig_header):
    """
    Process a Stripe webhook event asynchronously using Celery.

    This task verifies the webhook signature, executes the appropriate business
    logic, and handles retries automatically if an exception occurs.

    Args:
        payload (str): The raw webhook payload received from Stripe.
        sig_header (str): The Stripe-Signature header for webhook verification.

    Raises:
        self.retry: Retries the task in case of an exception, up to max_retries.
    """
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        executor = StripeWebhookExecutor(payload=payload, sig_header=sig_header)
        executor.verify_event()
        executor.execute()
    except Exception as e:
        self.retry(exc=e)
