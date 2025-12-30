from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.documents_contexts.permission import DocumentContextPermission


class DocumentContextAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and DocumentContext-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        DocumentContextPermission
    ]
