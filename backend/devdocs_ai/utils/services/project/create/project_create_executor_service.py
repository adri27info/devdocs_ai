from apps.projects.models import Project
from apps.notifications.models import Notification
from apps.users_projects.models import UserProject
from apps.roles_projects.models import RoleProject

from utils.general_utils import GeneralUtils


class ProjectCreateExecutorService:
    """
    Service to create a Project along with its owner and notifications.

    This service handles the creation of a Project instance, assigns the request user
    as the owner, and generates invitation notifications for additional users.
    Note that `UserProject` instances are only created for the owner. Other users
    must accept the invitation before being added to the project.

    Methods:
        run(request_user, validated_data):
            Creates the project, sets the owner, sends notifications, and returns
            the created Project instance.
    """

    @staticmethod
    def run(*, request_user, validated_data):
        """
        Create a project, assign owner, and send invitations.

        Args:
            request_user (User): The user making the request, who becomes the owner.
            validated_data (dict): Validated serializer data for the project.

        Returns:
            Project: The newly created Project instance.

        Raises:
            RoleProject.DoesNotExist: If "owner" or "member" roles do not exist.
        """
        users = validated_data.pop('users', [])

        if request_user not in users:
            users.append(request_user)

        validated_data["invitation_code"] = GeneralUtils.generate_invitation_code()
        project = Project.objects.create(**validated_data)

        owner_role = RoleProject.objects.get(name="owner")
        member_role = RoleProject.objects.get(name="member")

        for user in users:
            if user != request_user:
                Notification.objects.create(
                    sender=request_user,
                    receiver=user,
                    type="action_required",
                    action_required_reason="project_invitation",
                    message_reason=(
                        f"You have been invited to join a project - {project.name}."
                    )
                )

            role = owner_role if user == request_user else member_role

            if user == request_user:
                UserProject.objects.create(
                    user=user,
                    project=project,
                    role_project=role
                )

        return project
