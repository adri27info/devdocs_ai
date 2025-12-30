from rest_framework import permissions

from apps.documents.models import Document
from apps.users_projects.models import UserProject


class DocumentFeedbackPermission(permissions.BasePermission):
    """
    Permission class for creating and accessing DocumentFeedback objects.

    This permission enforces the following rules:

    - Safe methods (GET, HEAD, OPTIONS, TRACE): allowed for any authenticated user.
    - POST: allowed only if the user is a member of the project associated with the document.
      If the 'document' field is missing in the request, the check is deferred to the serializer.
    - Other unsafe methods (PUT, PATCH, DELETE) are denied.

    Methods:
        has_permission(request, view):
            Determines whether the user is allowed to access or create DocumentFeedback.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access or create DocumentFeedback.

        Args:
            request (Request): The HTTP request being processed.
            view (View): The view that is handling the request.

        Returns:
            bool: True if access is allowed, False otherwise.
                Safe methods are allowed for authenticated users.
                POST is allowed only for users who are members of the associated project.
                Other methods are denied.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == "POST":
            document_id = request.data.get("document")

            if not document_id:
                # let serializer handle the data validation
                return True

            project = Document.objects.filter(id=document_id).values_list(
                "document_context__project", flat=True
            ).first()

            if not project:
                return False

            user_project = UserProject.objects.filter(
                user=request.user,
                project=project
            ).select_related("role_project").first()

            return bool(user_project and user_project.role_project.name == "member")

        return False
