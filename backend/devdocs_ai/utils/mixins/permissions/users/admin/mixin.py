from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.users.admin.permission import IsAdminPermission


class AdminAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and Admin-User-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        IsAdminPermission
    ]
