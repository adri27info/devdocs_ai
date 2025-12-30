from rest_framework.exceptions import ValidationError


class BaseValidator:
    """
    Base class for custom validators that can raise DRF ValidationErrors.
    """

    def __init__(self, error_key=None):
        """
        Initializes the base validator with an optional error key.

        Args:
            error_key (str, optional): Key used in the ValidationError dictionary.
                Defaults to None.
        """
        self.error_key = error_key

    def raise_error(self, error_message):
        """
        Raises a DRF ValidationError with optional error key.

        Args:
            error_message (str): The error message to include in the exception.

        Raises:
            ValidationError: The DRF ValidationError constructed using the message
                and optional error key.
        """
        if self.error_key:
            raise ValidationError({self.error_key: [error_message]})
        else:
            raise ValidationError([error_message])
