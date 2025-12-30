from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.invoices.permission import InvoicePermission


class InvoiceAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and Invoice-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        InvoicePermission
    ]
