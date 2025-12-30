from rest_framework_simplejwt.exceptions import InvalidToken


class RefreshTokenBlacklistSetterService:
    """
    Service to add a refresh token to the blacklist.
    """

    @staticmethod
    def run(*, refresh_token):
        """
        Blacklists the provided refresh token.

        Args:
            refresh_token (RefreshToken): The token to blacklist.

        Raises:
            InvalidToken: If token cannot be blacklisted.
        """
        try:
            refresh_token.blacklist()
        except Exception:
            raise InvalidToken("Invalid refresh token: failed to blacklist.")
