from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.llms.permission import LLMPermission


class LLMAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and LLM-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        LLMPermission
    ]
