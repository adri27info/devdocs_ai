from utils.services.user.email.email_service import EmailService
from utils.general_utils import GeneralUtils


class ProjectUpdateHandlerService:
    """
    Service to handle post-processing actions after updating a project.
    """

    @staticmethod
    def run(*, serializer):
        """
        Send project invitation and removal emails after a project update.

        Sends an asynchronous invitation email to each user added to the project and
        a removal email to each user excluded from the project.

        Args:
            serializer (Serializer): Serializer containing the updated Project instance
                and the validated data with users_to_add and users_to_exclude.

        Raises:
            None: Errors related to email sending are handled internally by EmailService.
        """
        users_to_add = serializer.validated_data.get("users_to_add", [])
        users_to_exclude = serializer.validated_data.get("users_to_exclude", [])

        for user in users_to_add:
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

        for user in users_to_exclude:
            EmailService().send_email_task_async(
                email_type="project_removed",
                to_email=user.email,
                context=GeneralUtils.build_email_context(
                    user_email=user.email,
                    project_name=serializer.instance.name,
                    notifications_url=GeneralUtils.build_frontend_url(
                        path="notifications/information"
                    ),
                )
            )
