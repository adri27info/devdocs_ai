from rest_framework.response import Response


class ResponseCheckerTypeService:
    """
    Service to check if a given response is an instance of `Response`.
    """

    @staticmethod
    def run(*, response):
        """
        Checks if the provided response is an instance of `Response`.

        Args:
            response (Any): The response object to check.

        Returns:
            bool: True if the response is an instance of `Response`, False otherwise.
        """
        return isinstance(response, Response)
