from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.users.permission import UserPermission


class UserAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and User-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        UserPermission
    ]
