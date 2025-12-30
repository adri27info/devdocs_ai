from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.documents_feedbacks.permission import DocumentFeedbackPermission


class DocumentFeedbackAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and DocumentFeedback-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        DocumentFeedbackPermission
    ]
