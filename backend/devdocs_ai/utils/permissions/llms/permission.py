from rest_framework import permissions


class LLMPermission(permissions.BasePermission):
    """
    Permission class for accessing LLM-related endpoints.

    This permission enforces the following rules:

    - Safe methods (GET, HEAD, OPTIONS, TRACE) are allowed for authenticated users.
    - All other HTTP methods (POST, PUT, PATCH, DELETE) are denied.

    Methods:
        has_permission(request, view):
            Determines whether the user is allowed to access the view.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.

        Returns:
            bool: True if the request method is safe and the user is authenticated,
                False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return False
