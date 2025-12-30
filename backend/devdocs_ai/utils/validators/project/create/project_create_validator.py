from rest_framework import serializers

from apps.users_projects.models import UserProject


class ProjectCreateValidator:
    """
    Validator for project creation, enforcing plan and user limits.
    """

    @staticmethod
    def run(*, request_user, data):
        """
        Validate project creation rules for a user and project data.

        Checks the following rules:
        1. Free plan users cannot create private projects.
        2. Users cannot exceed the maximum number of projects allowed by their plan.
        3. Total users in a project (including the owner) cannot exceed plan limits.

        Args:
            request_user (User): The user making the project creation request.
            data (dict): Dictionary containing project creation fields, including
                'users' and 'privacy'.

        Raises:
            serializers.ValidationError: If any plan or user limits are exceeded.

        Returns:
            dict: The validated data, unmodified if all checks pass.
        """
        total_users = len(data.get('users', [])) + 1
        max_projects = request_user.plan_type.max_projects
        max_users_per_project = request_user.plan_type.max_users
        user_ids = {u.id if hasattr(u, "id") else u for u in data.get("users", [])}

        current_owned_projects_count = UserProject.objects.filter(
            user=request_user,
            role_project__name="owner"
        ).count()

        if request_user.id in user_ids:
            raise serializers.ValidationError(
                {
                    "detail": "You cannot include yourself in the users list."
                }
            )

        if request_user.plan_type.name == "free" and data.get("privacy") == "private":
            raise serializers.ValidationError(
                {
                    "detail": "You cannot create private projects with your current plan."
                }
            )

        if current_owned_projects_count >= max_projects:
            raise serializers.ValidationError(
                {
                    "detail": (
                        f"You cannot create more than {max_projects} "
                        "projects."
                    )
                }
            )

        if total_users > max_users_per_project:
            raise serializers.ValidationError(
                {
                    "detail": (
                        f"You cannot add more than {max_users_per_project} users to a project, "
                        "including yourself."
                    )
                }
            )

        return data
