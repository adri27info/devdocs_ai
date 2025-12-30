from rest_framework import permissions

from apps.projects.models import Project
from apps.users_projects.models import UserProject


class ProjectPermission(permissions.BasePermission):
    """
    Permission class for Project endpoints.

    This permission class enforces the following rules:

    - View-level access (`has_permission`):
        - Allowed for any authenticated user.
    - Object-level access (`has_object_permission`):
        - Safe methods (GET, HEAD, OPTIONS, TRACE) are allowed for any authenticated user.
        - Unsafe methods (POST, PUT, PATCH, DELETE) are allowed only for users
          who have the role "owner" in the corresponding project.

    Methods:
        has_permission(request, view):
            Determines whether the request should be allowed at the view level.
        has_object_permission(request, view, obj):
            Determines whether the request should be allowed at the object level.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access a specific Project object.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.
            obj (Project): The project object being accessed.

        Returns:
            bool: True if access is allowed, False otherwise. Safe methods
                are allowed for any authenticated user, while unsafe
                methods require the user to have an 'owner' role in the project.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if isinstance(obj, Project):
            user_project = UserProject.objects.filter(
                user=request.user,
                project=obj
            ).select_related("role_project").first()

            return bool(user_project and user_project.role_project.name == "owner")

        return False
