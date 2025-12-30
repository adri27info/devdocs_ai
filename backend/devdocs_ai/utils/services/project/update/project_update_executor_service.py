from apps.notifications.models import Notification
from apps.users_projects.models import UserProject


class ProjectUpdateExecutorService:
    """
    Service to handle additional updates after a project is updated,
    like sending notifications for added or excluded users.
    """

    @staticmethod
    def run(*, request_user, instance, users_to_add=None, users_to_exclude=None):
        """
        Send notifications to users added or excluded from the project,
        and remove excluded users from the project.

        Args:
            request_user: The user performing the update.
            instance: The Project instance that was updated.
            users_to_add: Iterable of User instances to add.
            users_to_exclude: Iterable of User instances to exclude.

        Returns:
            The updated Project instance (same as `instance`).
        """
        users_to_add = users_to_add or []
        users_to_exclude = users_to_exclude or []

        for user in users_to_exclude:
            UserProject.objects.filter(user=user, project=instance).delete()
            Notification.objects.create(
                sender=request_user,
                receiver=user,
                type="info",
                message_reason=(
                    f"You have been removed from the project: {instance.name}. "
                )
            )

        for user in users_to_add:
            Notification.objects.create(
                sender=request_user,
                receiver=user,
                type="action_required",
                action_required_reason="project_invitation",
                message_reason=(
                    f"You have been invited to join a project: {instance.name}."
                )
            )

        return instance
