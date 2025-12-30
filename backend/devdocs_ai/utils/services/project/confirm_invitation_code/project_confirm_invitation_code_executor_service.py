from apps.notifications.models import Notification
from apps.users_projects.models import UserProject


class ProjectConfirmInvitationCodeExecutorService:
    """
    Service to add a user to a project after confirming an invitation code.

    This class handles creating a UserProject record for the user with the
    "member" role, notifying the project owner that a new user has joined,
    and returning the owner instance.
    """

    @staticmethod
    def run(*, request_user, project, role_project):
        """
        Add a user to a project and notify the project owner.

        Creates a UserProject entry for the request_user with the given role.
        If the user was newly added, a notification is sent to the project owner.

        Args:
            request_user (User): The user joining the project.
            project (Project): The project the user is joining.
            role_project (RoleProject): The role to assign to the user in the project.

        Returns:
            User: The owner of the project.

        Raises:
            DatabaseOperationException: If the UserProject or Notification cannot
                be created.
        """
        _, created = UserProject.objects.get_or_create(
            user=request_user,
            project=project,
            defaults={"role_project": role_project}
        )

        if created:
            user_project_related = UserProject.objects.select_related(
                "user",
                "role_project"
            ).get(
                project=project,
                role_project__name="owner"
            )

            owner = user_project_related.user

            Notification.objects.create(
                sender=request_user,
                receiver=owner,
                type="info",
                message_reason=f"New user has joined your project - {project.name}."
            )

            return owner
