from utils.mixins.permissions.permissions_mixins import AuthWithRefreshAndCSRFPermissionMixin
from utils.permissions.projects.permission import ProjectPermission


class ProjectAuthPermissionMixin:
    """
    Combines authentication, refresh & CSRF token validation,
    and Project-specific permission logic in a reusable mixin.
    """
    permission_classes = [
        *AuthWithRefreshAndCSRFPermissionMixin.permission_classes,
        ProjectPermission
    ]
