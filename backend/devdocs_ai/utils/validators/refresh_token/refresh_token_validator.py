from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.users.models import User

from utils.general_utils import GeneralUtils


class RefreshTokenValidator:
    """
    Service to validate a refresh token and retrieve its associated user.
    """

    __REQUIRE_ACTIVE = True

    def __init__(self, *, require_active=None):
        """
        Initializes the service with optional active-user requirement.

        Args:
            require_active (bool, optional): Whether user must be active. Defaults True.
        """
        self.require_active = GeneralUtils.use_default_if_none(
            value=require_active,
            default=self.__REQUIRE_ACTIVE
        )

    def run(self, *, refresh_token_str):
        """
        Validates a refresh token string and retrieves the associated user.

        Args:
            refresh_token_str (str): The refresh token string to validate.

        Raises:
            InvalidToken: If token is malformed, expired, missing claims, or user
                is invalid/inactive.

        Returns:
            tuple: The validated RefreshToken instance and associated User.
        """
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except Exception:
            raise InvalidToken("Invalid refresh token: malformed or expired.")

        user_id = refresh_token.payload.get("user_id")

        if not user_id:
            raise InvalidToken("Invalid refresh token: missing user_id claim.")

        user = User.objects.filter(id=user_id).first()

        if not user:
            raise InvalidToken("Invalid refresh token: user not found.")

        if self.require_active and not user.is_active:
            raise InvalidToken("Invalid refresh token: user account is inactive.")

        return refresh_token, user
