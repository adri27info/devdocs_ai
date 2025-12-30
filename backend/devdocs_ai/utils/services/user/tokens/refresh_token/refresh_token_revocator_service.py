from utils.services.user.tokens.refresh_token.black_list.\
    refresh_token_black_list_setter_service \
    import RefreshTokenBlacklistSetterService

from utils.validators.refresh_token.refresh_token_pre_validator import (
    RefreshTokenPreValidator
)

from utils.general_utils import GeneralUtils


class RefreshTokenRevocatorService:
    """
    Service to validate and optionally revoke a refresh token."""

    __REQUIRE_ACTIVE = True
    __REVOKE = True

    def __init__(self, *, require_active=None, revoke=None):
        """
        Initializes the revocator with optional active check and revoke flag.

        Args:
            require_active (bool, optional): Whether user must be active. Defaults True.
            revoke (bool, optional): Whether to revoke token after validation.
                Defaults to True.
        """
        self.require_active = GeneralUtils.use_default_if_none(
            value=require_active,
            default=self.__REQUIRE_ACTIVE
        )
        self.revoke = GeneralUtils.use_default_if_none(
            value=revoke,
            default=self.__REVOKE
        )

    def run(self, *, request):
        """
        Validates and optionally revokes a refresh token from request cookies.

        Args:
            request (HttpRequest): Django request object with the refresh token.

        Returns:
            User: The user associated with the refresh token.
        """
        refresh_token_obj, user = RefreshTokenPreValidator(
            require_active=self.require_active
        ).run(
            request=request
        )

        if self.revoke:
            RefreshTokenBlacklistSetterService.run(
                refresh_token=refresh_token_obj
            )

        return user
