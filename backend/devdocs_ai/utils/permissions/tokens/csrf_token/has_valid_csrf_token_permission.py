from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from utils.services.user.tokens.cookie.csrf_token.cookie_csrf_token_checker_service import (
    CookieCSRFTokenCheckerService
)


class HasValidCSRFTokenPermission(BasePermission):
    """
    Permission to allow access only if a valid CSRF token is present.
    """

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS', 'TRACE')

    def has_permission(self, request, view):
        """
        Checks if the request contains a valid CSRF token for unsafe methods.

        Args:
            request (HttpRequest): The current request object.
            view (View): The view being accessed.

        Raises:
            PermissionDenied: If CSRF token is missing, expired, or mismatched.

        Returns:
            bool: True if CSRF token is valid or method is safe.
        """
        if request.method in self.SAFE_METHODS:
            return True

        if not CookieCSRFTokenCheckerService.run(
            request=request
        ):
            raise PermissionDenied(
                "Invalid csrf token: missing, expired or mismatch."
            )

        return True
