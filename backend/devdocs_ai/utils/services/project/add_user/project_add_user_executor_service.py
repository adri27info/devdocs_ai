from apps.notifications.models import Notification

from utils.general_utils import GeneralUtils


class ProjectAddUserExecutorService:
    """
    Service to execute adding a user to a project.

    This class handles the side effects after a user is added to a project, such as
    generating a new invitation code and creating a notification for the added user.
    """

    @staticmethod
    def run(*, instance, request_user, user):
        """
        Execute the addition of a user to a project.

        This method updates the project's invitation code and sends a notification to
        the added user.

        Args:
            instance (Project): The project instance to update.
            request_user (User): The user performing the action.
            user (User): The user being added to the project.

        Returns:
            None
        """
        instance.invitation_code = GeneralUtils.generate_invitation_code()
        instance.save(update_fields=['invitation_code'])

        Notification.objects.create(
            sender=request_user,
            receiver=user,
            type="action_required",
            action_required_reason="project_invitation",
            message_reason=f"You have been invited to join a project - {instance.name}."
        )
