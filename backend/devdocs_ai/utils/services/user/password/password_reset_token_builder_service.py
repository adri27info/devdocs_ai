from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordResetTokenBuilderService:
    """
    Service to generate UID and password reset token for a user.
    """

    __TOKEN_GENERATOR = PasswordResetTokenGenerator()

    @classmethod
    def run(cls, *, user):
        """
        Generates a UID and password reset token for the given user.

        Args:
            user (User): The user instance to generate token for.

        Returns:
            dict: Dictionary containing 'uid' and 'token'.
        """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = cls.__TOKEN_GENERATOR.make_token(user)

        return {
            "uid": uid,
            "token": token,
        }
