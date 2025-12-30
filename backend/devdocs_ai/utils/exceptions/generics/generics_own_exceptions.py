from rest_framework import status


class AppBaseException(Exception):
    """
    Base exception class for the application.

    Attributes:
        status_code (int): HTTP status code associated with the exception.
        default_detail (str): Default error message.
        detail (str): Actual error message provided during initialization.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An unexpected error occurred."

    def __init__(self, detail=None):
        """
        Initialize the exception with an optional custom detail message.

        Args:
            detail (str, optional): Custom error message. Defaults to None.
        """
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class BadRequestException(AppBaseException):
    """
    Exception raised for HTTP 400 Bad Request errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."


class UnauthorizedException(AppBaseException):
    """
    Exception raised for HTTP 401 Unauthorized errors.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication required."


class NotFoundException(AppBaseException):
    """
    Exception raised for HTTP 404 Not Found errors.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found."


class ConflictException(AppBaseException):
    """
    Exception raised for HTTP 409 Conflict errors.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict with the current state of the resource."


class InternalServerErrorException(AppBaseException):
    """
    Exception raised for HTTP 500 Internal Server Error.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Internal server error."
