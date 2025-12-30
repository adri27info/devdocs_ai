from utils.services.user.tokens.refresh_token.black_list import (
    refresh_token_black_list_checker_service as refresh_token_utility,
)
from utils.validators.refresh_token.refresh_token_validator import (
    RefreshTokenValidator
)
from utils.general_utils import GeneralUtils


class RefreshTokenPreValidator:
    """
    Service to validate refresh tokens and check against the blacklist.
    """

    __REFRESH_TOKEN_COOKIE_KEY = "refreshtoken"
    __REQUIRE_ACTIVE = True

    def __init__(self, *, require_active=None):
        """
        Initializes the validator with an optional requirement for active user.

        Args:
            require_active (bool, optional): Whether the user must be active.
                Defaults to True.
        """
        self.require_active = GeneralUtils.use_default_if_none(
            value=require_active,
            default=self.__REQUIRE_ACTIVE
        )

    def run(self, *, request):
        """
        Validates the refresh token from request cookies and checks blacklist.

        Args:
            request (HttpRequest): The Django request object containing cookies.

        Returns:
            tuple: The validated RefreshToken instance and associated User.
        """
        refresh_token_obj, user = RefreshTokenValidator(
            require_active=self.require_active
        ).run(
            refresh_token_str=request.COOKIES.get(self.__REFRESH_TOKEN_COOKIE_KEY)
        )

        refresh_token_utility.RefreshTokenBlacklistCheckerService.ensure_not_blacklisted(
            refresh_token=refresh_token_obj
        )

        return refresh_token_obj, user
