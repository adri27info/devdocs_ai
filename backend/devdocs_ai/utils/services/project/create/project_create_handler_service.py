from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ProjectCreateHandlerService:
    """
    Service to handle post-processing actions after creating a project.
    """

    @staticmethod
    def run(*, request_user, serializer):
        """
        Send project invitation emails to invited users.

        Iterates through all users in the validated serializer data and sends an
        asynchronous invitation email to each user except the request user.

        Args:
            request_user (User): The user who created the project and triggered the action.
            serializer (Serializer): Serializer containing the created Project instance
                and the validated data with invited users.

        Raises:
            None: Errors related to email sending should be handled internally by EmailService.
        """
        invited_users = serializer.validated_data.get("users", [])

        for user in invited_users:
            if user != request_user:
                EmailService().send_email_task_async(
                    email_type="project_invitation",
                    to_email=user.email,
                    context=GeneralUtils.build_email_context(
                        user_email=user.email,
                        project_name=serializer.instance.name,
                        invitation_code=serializer.instance.invitation_code,
                        notifications_url=GeneralUtils.build_frontend_url(
                            path="notifications/action-required"
                        ),
                    )
                )
