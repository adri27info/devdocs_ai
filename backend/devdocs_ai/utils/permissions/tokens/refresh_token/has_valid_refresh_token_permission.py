from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from utils.services.user.tokens.cookie.refresh_token.cookie_refresh_token_getter_service import (
    CookieRefreshTokenGetterService
)


class HasValidRefreshTokenPermission(BasePermission):
    """
    Permission to allow access only if a valid refresh token is present.
    """

    def has_permission(self, request, view):
        """
        Checks if the request contains a valid refresh token.

        Args:
            request (HttpRequest): The current request object.
            view (View): The view being accessed.

        Raises:
            PermissionDenied: If refresh token is missing or invalid.

        Returns:
            bool: True if the refresh token is valid, False otherwise.
        """
        if not CookieRefreshTokenGetterService.run(
            request=request
        ):
            raise PermissionDenied(
                "Invalid refresh token: token missing or expired."
            )
        return True
