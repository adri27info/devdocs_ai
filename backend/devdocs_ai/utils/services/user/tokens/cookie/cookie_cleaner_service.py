from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException


class CookieCleanerService:
    """
    Service to clear authentication-related cookies from a Django response."""

    @staticmethod
    def run(*, response):
        """
        Deletes standard authentication cookies from the response.

        Args:
            response (HttpResponse): The Django response object to clear cookies from.

        Raises:
            InstanceInvalidValueException: If response is invalid or missing.

        Returns:
            HttpResponse: The modified response with cookies cleared.
        """
        if not response:
            raise InstanceInvalidValueException("Invalid or missing response param.")

        cookies_to_clear = ["accesstoken", "refreshtoken", "csrftoken"]

        for cookie_name in cookies_to_clear:
            response.delete_cookie(cookie_name, path="/")

        return response
