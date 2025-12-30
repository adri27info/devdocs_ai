from rest_framework import permissions

from apps.notifications.models import Notification


class NotificationPermission(permissions.BasePermission):
    """
    Permission class for accessing Notification objects.

    This permission enforces the following rules:

    - GET, HEAD, OPTIONS, TRACE (safe methods) are allowed only for authenticated users.
    - Other methods are not allowed at the endpoint level.
    - For object-level access:
        - Safe methods: allowed if the user is authenticated.
        - Unsafe methods: allowed only if the user is the receiver of the notification.
    """

    def has_permission(self, request, view):
        """
        Determine if the request has permission to access the view.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == "DELETE":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Determine if the request has permission to access a specific object.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.
            obj (Model): The object being accessed.

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if isinstance(obj, Notification):
            return obj.receiver == request.user

        return False
