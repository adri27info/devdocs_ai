from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ProjectAddUserHandlerService:
    """
    Service to handle sending email notifications when a user is added to a project.

    This service is responsible for building the email context and sending an
    asynchronous email invitation to the user with the project details and
    invitation code.
    """

    @staticmethod
    def run(*, user, project):
        """
        Send a project invitation email to a user.

        Args:
            user (User): The user who is being added to the project.
            project (Project): The project instance the user is being added to.

        Returns:
            None
        """
        EmailService().send_email_task_async(
            email_type="project_invitation",
            to_email=user.email,
            context=GeneralUtils.build_email_context(
                user_email=user.email,
                project_name=project.name,
                invitation_code=project.invitation_code,
                notifications_url=GeneralUtils.build_frontend_url(
                    path="notifications/action-required"
                ),
            )
        )
