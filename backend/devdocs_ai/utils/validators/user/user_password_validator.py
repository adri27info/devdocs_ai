import re

from utils.validators.base.base_validator import BaseValidator


class UserPasswordValidator(BaseValidator):
    """
    Validator to enforce password complexity requirements.
    """

    def __init__(self, error_key=None):
        """
        Initializes the password validator.

        Args:
            error_key (str, optional): Custom key for error messages.
        """
        super().__init__(error_key=error_key)

    def __call__(self, value):
        """
        Validates the password according to complexity rules.

        Args:
            value (str): Password to validate.

        Raises:
            ValidationError: If password fails any complexity requirement.
        """
        if len(value) < 8 or len(value) > 20:
            self.raise_error(
                error_message="Password must be between 8 and 20 characters long."
            )

        if not re.search(r"[A-Z]", value):
            self.raise_error(
                error_message="Password must contain at least one uppercase letter."
            )

        if not re.search(r"\d", value):
            self.raise_error(
                error_message="Password must contain at least one number."
            )

        if not re.search(r"[\W_]", value):
            self.raise_error(
                error_message="Password must contain at least one special character."
            )

        if re.search(r"\s", value):
            self.raise_error("Password cannot contain spaces.")
