from rest_framework import status

from utils.exceptions.generics.generics_own_exceptions import InternalServerErrorException


class DatabaseOperationException(InternalServerErrorException):
    """
    Raised when a database operation fails unexpectedly.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A database error occurred while processing the request."
