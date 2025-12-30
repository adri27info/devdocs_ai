from rest_framework.response import Response
from rest_framework import status


class ExceptionResponseHandlerService:
    """
    Service to convert exceptions into DRF Response objects.
    """

    @staticmethod
    def run(*, exc):
        """
        Convert an exception to a DRF Response with a `detail` key.

        Args:
            exc (Exception): The exception instance to convert.

        Returns:
            Response: DRF Response containing the error detail and status code.
        """

        detail = getattr(exc, "detail", str(exc))
        status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if isinstance(detail, dict) and "detail" not in detail:
            return Response(detail, status=status_code)

        if isinstance(detail, dict) and "detail" in detail:
            detail = detail["detail"]

        return Response({"detail": detail}, status=status_code)
