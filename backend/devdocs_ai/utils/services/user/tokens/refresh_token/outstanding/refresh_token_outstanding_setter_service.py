from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenOutstandingSetterService:
    """
    Service to handle outstanding refresh tokens.
    """

    @staticmethod
    def run(*, refresh_token_str):
        """
        Marks a refresh token as outstanding.

        Args:
            refresh_token_str (str): The refresh token string to mark.
        """
        refresh_token = RefreshToken(refresh_token_str)
        refresh_token.outstand()
