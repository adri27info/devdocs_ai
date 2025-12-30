from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.payments.permission import PaymentPermission


class PaymentAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and PaymentPermission-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        PaymentPermission
    ]
