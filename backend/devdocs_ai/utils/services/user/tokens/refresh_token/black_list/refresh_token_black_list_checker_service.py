from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken


class RefreshTokenBlacklistCheckerService:
    """
    Service to check whether a refresh token is blacklisted.
    """

    @classmethod
    def is_blacklisted(cls, *, refresh_token):
        """
        Checks if the refresh token is blacklisted.

        Args:
            refresh_token (RefreshToken): Token to check.

        Raises:
            InvalidToken: If the token is missing the 'jti' claim.

        Returns:
            bool: True if token is blacklisted, False otherwise.
        """
        jti = refresh_token.payload.get("jti")
        if not jti:
            raise InvalidToken("Invalid refresh token: missing jti claim.")

        return BlacklistedToken.objects.filter(token__jti=jti).exists()

    @classmethod
    def ensure_not_blacklisted(cls, *, refresh_token):
        """
        Ensures the refresh token is not blacklisted.

        Args:
            refresh_token (RefreshToken): Token to validate.

        Raises:
            InvalidToken: If the token is blacklisted.
        """
        if cls.is_blacklisted(refresh_token=refresh_token):
            raise InvalidToken("Invalid refresh token: token is blacklisted.")
