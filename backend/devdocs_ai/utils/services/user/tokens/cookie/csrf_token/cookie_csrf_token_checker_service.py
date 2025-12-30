class CookieCSRFTokenCheckerService:
    """
    Service to validate the CSRF token by comparing cookie and header.
    """

    @staticmethod
    def run(*, request):
        """
        Validates that the CSRF cookie matches the X-CSRFToken header.

        Args:
            request (HttpRequest): Django request object.

        Returns:
            bool: True if CSRF token is present and valid, False otherwise.
        """
        csrf_cookie = request.COOKIES.get('csrftoken')
        csrf_header = request.headers.get('X-CSRFToken')

        if not csrf_cookie or not csrf_header:
            return False

        return csrf_cookie == csrf_header
