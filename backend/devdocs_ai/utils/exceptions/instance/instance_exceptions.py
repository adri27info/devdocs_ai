from rest_framework import status

from utils.exceptions.generics.generics_own_exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
    InternalServerErrorException
)


class InstanceInvalidValueException(BadRequestException):
    """
    Raised when an instance exists but its current state does not allow the operation.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The resource instance is in an invalid state for this operation."


class InstanceUnexpectedValueException(BadRequestException):
    """
    Raised when an instance has a value that does not match the expected value.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The resource instance has an unexpected value."


class InstanceNotFoundException(NotFoundException):
    """
    Raised when a required instance does not exist in the database.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested resource instance does not exist."


class InstanceAlreadyExistsException(ConflictException):
    """
    Raised when trying to create an instance that already exists in the database.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "The resource instance already exists."


class InstanceInternalErrorException(InternalServerErrorException):
    """
    Raised when an internal error occurs related to an instance
    (e.g., bucket unavailable, storage error, etc.).
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An internal error occurred with the resource instance."
