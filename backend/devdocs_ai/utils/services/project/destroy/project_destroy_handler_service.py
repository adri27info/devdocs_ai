from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ProjectDestroyHandlerService:
    """
    Service to send project deletion emails asynchronously to associated users.
    """

    @staticmethod
    def run(*, associated_users, instance, request_user):
        """
        Send emails notifying users that the project has been deleted.

        Args:
            associated_users (list[User]): Users associated with the project.
            instance (Project): The project instance that was deleted.

        Returns:
            None
        """
        for user in associated_users:
            if user != request_user:
                EmailService().send_email_task_async(
                    email_type="project_deleted",
                    to_email=user.email,
                    context=GeneralUtils.build_email_context(
                        user_email=user.email,
                        project_name=instance.name,
                        notifications_url=GeneralUtils.build_frontend_url(
                            path="notifications/information"
                        ),
                    )
                )
