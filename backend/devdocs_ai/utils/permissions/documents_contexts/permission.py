from rest_framework import permissions

from apps.users_projects.models import UserProject


class DocumentContextPermission(permissions.BasePermission):
    """
    Permission for creating and accessing DocumentContext objects.

    This permission class enforces the following rules:

    - GET (and other safe methods like HEAD, OPTIONS): allowed for any authenticated user.
    - POST: allowed only for users who are members of the project with the role "owner".
    - Other unsafe methods (PUT, PATCH, DELETE): not allowed by default.

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
            bool: True if access is allowed, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == "POST":
            project_id = request.data.get("project")

            if not project_id:
                # let serializer handle the data validation
                return True

            user_project = UserProject.objects.filter(
                user=request.user,
                project_id=project_id
            ).select_related("role_project").first()

            return bool(user_project and user_project.role_project.name == "owner")

        return False
