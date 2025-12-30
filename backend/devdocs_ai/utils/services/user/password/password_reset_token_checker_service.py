from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.users.models import User


class PasswordResetTokenCheckerService:
    """
    Service to validate user ID and password reset token."""

    __TOKEN_GENERATOR = PasswordResetTokenGenerator()

    @classmethod
    def run(cls, *, uid, token):
        """
        Validates the UID and token and returns the corresponding user.

        Args:
            uid (str): Base64-encoded user ID.
            token (str): Password reset token.

        Returns:
            User | None: User instance if token is valid, None otherwise.
        """
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)

        if cls.__TOKEN_GENERATOR.check_token(user, token):
            return user

        return None
