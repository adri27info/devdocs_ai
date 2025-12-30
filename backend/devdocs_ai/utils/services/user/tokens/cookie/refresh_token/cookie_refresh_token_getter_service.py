class CookieRefreshTokenGetterService:
    """
    Service to check for the presence of a refresh token in request cookies.
    """

    @staticmethod
    def run(*, request):
        """
        Checks if a refresh token cookie exists in the request.

        Args:
            request (HttpRequest): Django request object.

        Returns:
            bool: True if refresh token exists, False otherwise.
        """
        refresh_token = request.COOKIES.get("refreshtoken")

        if not refresh_token:
            return False

        return True
