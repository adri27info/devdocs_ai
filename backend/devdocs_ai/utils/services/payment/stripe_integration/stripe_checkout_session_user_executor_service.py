from utils.exceptions.instance.instance_exceptions import InstanceUnexpectedValueException


class StripeCheckoutSessionUserExecutorService:
    """
    Service to validate that a Stripe Checkout Session belongs to the authenticated user.
    """

    @staticmethod
    def run(*, session_metadata, user_id):
        """
        Check if the session belongs to the given user.

        Args:
            session_metadata (dict): Metadata from Stripe Checkout Session.
            user_id (int or str): ID of the authenticated user.

        Raises:
            InstanceInvalidValueException: If session does not belong to the user.
        """
        session_user_id = session_metadata.get("user_id")

        if str(session_user_id) != str(user_id):
            raise InstanceUnexpectedValueException("This session does not belong to the user.")
