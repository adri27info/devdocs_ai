from rest_framework import permissions


class PaymentPermission(permissions.BasePermission):
    """
    Permission class for accessing Payment endpoints.

    This permission enforces the following rules:

    - Safe methods (GET, HEAD, OPTIONS, TRACE) are allowed only for authenticated users.
    - POST requests are allowed for any user (additional validation should be handled in the
    serializer or view).
    - Other HTTP methods (PUT, PATCH, DELETE, etc.) are denied by default.

    Methods:
        has_permission(request, view):
            Determines whether the request has permission at the view level.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == "POST":
            return True

        return False
