from rest_framework.permissions import AllowAny, IsAuthenticated

from utils.permissions.headers.has_valid_origin_header_permission import (
    HasValidOriginHeader
)
from utils.permissions.tokens.csrf_token.has_valid_csrf_token_permission import (
    HasValidCSRFTokenPermission
)
from utils.permissions.tokens.refresh_token.has_valid_refresh_token_permission import (
    HasValidRefreshTokenPermission
)


class NoPermissionsMixin:
    """
    Mixin to apply no permissions to a view.
    """
    permission_classes = []


class AllowAnyPermissionMixin:
    """
    Mixin to allow unrestricted access to a view.
    """
    permission_classes = [AllowAny]


class RefreshPermissionMixin:
    """
    Mixin to enforce valid refresh token permission only.
    """
    permission_classes = [HasValidRefreshTokenPermission]


class OriginHeaderPermissionMixin:
    """
    Mixin to enforce valid Origin header permission only.
    """
    permission_classes = [HasValidOriginHeader]


class AuthWithRefreshPermissionMixin:
    """
    Mixin for authenticated users with valid refresh token.
    """
    permission_classes = [
        IsAuthenticated,
        HasValidRefreshTokenPermission
    ]


class AuthWithCSRFPermissionMixin:
    """
    Mixin for authenticated users with valid CSRF token.
    """
    permission_classes = [
        IsAuthenticated,
        HasValidCSRFTokenPermission
    ]


class AuthWithRefreshAndCSRFPermissionMixin:
    """
    Mixin for authenticated users with both refresh and CSRF tokens.
    """
    permission_classes = [
        IsAuthenticated,
        HasValidRefreshTokenPermission,
        HasValidCSRFTokenPermission,
    ]
