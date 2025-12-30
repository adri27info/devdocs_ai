from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ProjectConfirmInvitationCodeHandlerService:
    """
    Service to handle post-confirmation actions after a user joins a project.

    This service is responsible for sending a notification email to the project owner
    when a new user joins their project via a confirmed invitation code.
    """

    @staticmethod
    def run(*, owner, project):
        """
        Send an email notification to the project owner.

        If an owner is provided, sends an asynchronous email notifying that a new
        user has joined the project.

        Args:
            owner (User): The owner of the project to notify.
            project (Project): The project that the new user has joined.
        """
        if owner:
            EmailService().send_email_task_async(
                email_type="project_joined",
                to_email=owner.email,
                context=GeneralUtils.build_email_context(
                    user_email=owner.email,
                    project_name=project.name,
                    notifications_url=GeneralUtils.build_frontend_url(
                        path="notifications/information"
                    ),
                )
            )
