from django.utils import timezone

from rest_framework import serializers

from apps.projects.models import Project
from apps.users_projects.models import UserProject


class ProjectConfirmInvitationCodeValidator:
    """
    Validator for confirming a user's project invitation code.

    This class provides a static method to validate that a user can join a project
    using an invitation code. It checks that the code exists, is not expired and the
    user is not already a member
    """

    @staticmethod
    def run(*, invitation_code, request_user):
        """
        Validate a user's project invitation code and return the project instance.

        Checks that the invitation code exists, is not expired and the user is not yet a
        member

        Args:
            invitation_code (str): The invitation code provided by the user.
            request_user (User): The user attempting to confirm the invitation.

        Raises:
            serializers.ValidationError: If the code is invalid, expired or the user is
                already a member

        Returns:
            Project: The project instance associated with the valid invitation code.
        """
        project = Project.objects.filter(
            invitation_code=invitation_code
        ).first()

        if not project:
            raise serializers.ValidationError(
                {
                    "detail": "Project with this invitation code does not exist."
                }
            )

        if project.invitation_code_expires_at < timezone.now():
            raise serializers.ValidationError(
                {
                    "detail": "Invitation code has expired."
                }
            )

        if UserProject.objects.filter(
            user=request_user,
            project=project
        ).exists():
            raise serializers.ValidationError(
                {
                    "detail": "You are already a member of this project."
                }
            )

        return project
