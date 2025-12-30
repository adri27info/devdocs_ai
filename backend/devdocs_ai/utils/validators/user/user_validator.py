from rest_framework import serializers


class UserValidator:
    """
    Validator to check user instance existence, activity, and password.
    """

    @staticmethod
    def run(*, user, password=None):
        """
        Validates a user instance for existence, active status, and password.

        Args:
            user (User): User instance to validate.
            password (str, optional): Password to check against the user instance.

        Raises:
            serializers.ValidationError: If user does not exist, is inactive, or
                password is incorrect.
        """
        if not user:
            raise serializers.ValidationError(
                {"detail": "User with this email does not exist."}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "This account is inactive. Please activate your account."}
            )

        if password is not None and not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "Email or password incorrect."}
            )
