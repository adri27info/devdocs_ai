from apps.notifications.models import Notification
from apps.users_projects.models import UserProject


class ProjectDestroyTransactionService:
    """
    Service to delete a project and create notifications for all associated users.
    """

    @staticmethod
    def run(*, instance, request_user):
        """
        Delete a project and create info notifications for users except the actor.

        Args:
            instance (Project): The project instance to delete.
            request_user (User): The user performing the deletion.

        Returns:
            list[User]: List of users associated with the project.
        """
        user_projects = UserProject.objects.filter(project=instance).select_related("user")
        associated_users = [up.user for up in user_projects]

        instance.delete()

        for user in associated_users:
            if user != request_user:
                Notification.objects.create(
                    sender=request_user,
                    receiver=user,
                    type="info",
                    message_reason=(
                        f"You have been removed from the project - {instance.name} "
                        "because the owner deleted the project."
                    )
                )

        return associated_users
