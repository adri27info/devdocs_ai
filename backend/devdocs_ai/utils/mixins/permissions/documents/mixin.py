from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.documents.permission import DocumentPermission


class DocumentAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and Document-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        DocumentPermission
    ]
