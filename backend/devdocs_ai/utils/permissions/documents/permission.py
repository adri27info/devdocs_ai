from rest_framework import permissions


class DocumentPermission(permissions.BasePermission):
    """
    Permission class for accessing Document objects.

    This permission enforces the following rules:

    - Safe methods (GET, HEAD, OPTIONS, TRACE): allowed for any authenticated user.
    - Other HTTP methods (POST, PUT, PATCH, DELETE) are denied.

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
            bool: True if access is allowed, False otherwise.
                Only allows authenticated users for safe methods.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return False
