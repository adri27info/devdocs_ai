from rest_framework import permissions

from apps.users.models import User


class UserPermission(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users and
    restrict object-level modifications to the owning user.

    This permission class enforces the following rules:
    - Any request requires the user to be authenticated.
    - Safe methods (GET, HEAD, OPTIONS) are allowed for any authenticated user.
    - Unsafe methods (PUT, PATCH, DELETE, etc.) are only allowed if the object
      being accessed is a ``User`` instance and corresponds to the requesting user.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated at the request level.

        Args:
            request (Request): The incoming HTTP request.
            view (APIView): The view being accessed.

        Returns:
            bool: ``True`` if the user is authenticated, ``False`` otherwise.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions.

        Safe methods are allowed for any authenticated user. For unsafe methods,
        permission is granted only if the object is a ``User`` instance and
        matches the requesting user.

        Args:
            request (Request): The incoming HTTP request.
            view (APIView): The view being accessed.
            obj (Any): The object being accessed.

        Returns:
            bool: ``True`` if the user has permission to access the object,
            ``False`` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if isinstance(obj, User):
            return obj == request.user

        return False
