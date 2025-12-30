from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.notifications.permission import NotificationPermission


class NotificationAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and Notification-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        NotificationPermission
    ]
