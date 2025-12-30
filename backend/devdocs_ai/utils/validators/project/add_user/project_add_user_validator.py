from rest_framework import serializers

from apps.users_projects.models import UserProject


class ProjectAddUserValidator:
    """
    Validator for adding a user to a project.

    This class provides a static method to validate whether a user can be added to a
    selected project based on business rules such as plan restrictions, duplicate
    membership, maximum project users, and allowed number of selected projects.
    """

    @staticmethod
    def run(*, data, request_user, max_users_per_project):
        """
        Validate adding a user to a project.

        Args:
            data (dict): Dictionary containing 'projects_selected' and 'user'.
            request_user (User): The user making the request.
            max_users_per_project (int): Maximum allowed users for the project.

        Raises:
            serializers.ValidationError: If any of the following conditions are met:
                1. More than one project is selected.
                2. The request user is trying to add themselves.
                3. The request user's plan does not allow adding users.
                4. The user is already a member of the selected project.
                5. The project has reached its maximum number of users.
        """
        projects_selected = data.get('projects_selected')
        user = data.get('user')

        if len(projects_selected) > 1:
            raise serializers.ValidationError(
                {
                    "projects_selected": "You can select only one project."
                }
            )

        project = projects_selected[0]

        if request_user.id == user.id:
            raise serializers.ValidationError(
                {
                    "detail": "You cannot add yourself to the project."
                }
            )

        if request_user.plan_type.name == "free":
            raise serializers.ValidationError(
                {
                    "detail": "You cannot add user according to your plan."
                }
            )

        if UserProject.objects.filter(
            user=user,
            project=project,
            role_project__name="member"
        ).exists():
            raise serializers.ValidationError(
                {
                    "detail": "User already exists in the project."
                }
            )

        current_users_count = UserProject.objects.filter(
            project=project
        ).count()

        if current_users_count >= max_users_per_project:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "You cannot add more users to this project because you reached "
                        "the max for the project."
                    )
                }
            )

        data["project"] = project
        return data
