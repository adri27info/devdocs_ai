from apps.invoices.models import Invoice
from apps.plans_types.models import PlanType

from utils.exceptions.instance.instance_exceptions import (
    InstanceNotFoundException,
    InstanceInvalidValueException,
    InstanceAlreadyExistsException,
)


class StripeCheckoutSessionUserValidator:
    """
    Validator for safely preparing a Stripe Checkout session.

    This service ensures that the Stripe API key is valid (unless explicitly skipped),
    the user exists and is active, a premium plan is available, and no invoice already
    exists for the given user. It raises detailed exceptions when validation fails and
    returns the premium plan instance if all checks pass.
    """

    @staticmethod
    def run(*, stripe_api_key, user, skip_stripe_api_key=False):
        """
        Executes all validations required before creating a Stripe Checkout session.

        Args:
            stripe_api_key (str): Stripe secret key used for API communication.
            user (User): Django User instance initiating the payment.
            skip_stripe_api_key (bool, optional): If True, skips API key validation.
                Defaults to False.

        Returns:
            PlanType: The premium plan instance that should be used for the session.

        Raises:
            InstanceNotFoundException: If the user, or premium plan is missing.
            InstanceInvalidValueException: If the user is inactive.
            InstanceAlreadyExistsException: If the user already has an invoice.
        """
        if not skip_stripe_api_key:
            if not stripe_api_key:
                raise InstanceInvalidValueException("Stripe API key is invalid.")

        if not user:
            raise InstanceNotFoundException(
                "User does not exist so the payment cannot be processed."
            )

        if not user.is_active:
            raise InstanceInvalidValueException(
                "User is inactive so the payment cannot be processed."
            )

        plan_type = PlanType.objects.filter(name="premium").first()

        if not plan_type:
            raise InstanceNotFoundException(
                "Premium plan type does not exist so the payment cannot be processed."
            )

        if Invoice.objects.filter(user=user).exists():
            raise InstanceAlreadyExistsException(
                "Invoice already exists for this user so the payment cannot be processed."
            )

        return plan_type
