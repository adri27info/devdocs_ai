from django.urls import path

from apps.payments.views.stripe_checkout_session_view import StripeCheckoutSessionView
from apps.payments.views.stripe_payment_status_view import StripePaymentStatusView
from apps.payments.views.stripe_webhook_view import StripeWebhookView

urlpatterns = [
    path("checkout_session/", StripeCheckoutSessionView.as_view(), name="checkout_session"),
    path("status/", StripePaymentStatusView.as_view(), name="payment_status"),
    path("webhook/", StripeWebhookView.as_view(), name="webhook"),
]
