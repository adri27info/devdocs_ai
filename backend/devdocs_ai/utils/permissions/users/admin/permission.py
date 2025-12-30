from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """
    Permission that grants access only to users with the admin role.

    This permission checks the authenticated user's role and allows access only
    if the role name is equal to "admin". It is evaluated after general
    permissions and is the final step before access is granted when an object is
    involved in the request.
    """

    def has_permission(self, request, view):
        """
        Check general access based on the user's admin role.

        This method is executed before any action and serves as the initial permission
        check for the view. It allows access only when the authenticated user's role
        name is "admin".

        Args:
            request (Request): The incoming HTTP request containing the user.
            view (APIView): The view that triggered this permission check.

        Returns:
            bool: True if the user's role is admin, otherwise False.
        """
        return request.user.role.name == "admin"

    def has_object_permission(self, request, view, obj):
        """
        Check object-level access based on the user's role.

        This method is executed after has_permission and serves as the last
        authorization step before granting access to the requested object. It
        returns True only when the authenticated user's role name is "admin".

        Args:
            request (Request): The incoming HTTP request containing the user.
            view (APIView): The view that triggered this permission check.
            obj (Any): The object that the user is attempting to access.

        Returns:
            bool: True if the user's role is admin, otherwise False.
        """
        return request.user.role.name == "admin"
