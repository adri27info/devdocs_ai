from rest_framework import serializers

from apps.users_projects.models import UserProject


class ProjectUpdateValidator:
    """
    Validator class to check project update rules for adding and excluding users.
    """
    @staticmethod
    def run(*, request_user, proyectInstance, data):
        """
        Validate the users to add or exclude when updating a project.

        This method checks for:
        - The request user is not in `users_to_add` or `users_to_exclude`.
        - No user is both added and excluded in the same request.
        - Users to add are not already part of the project.
        - Users to exclude are currently in the project.
        - Total number of users after the update does not exceed the user's plan limit.

        Args:
            request_user (User): The user performing the update.
            proyectInstance (Project): The project instance being updated.
            data (dict): The validated data from the serializer, containing keys
                         'users_to_add' and 'users_to_exclude'.

        Raises:
            serializers.ValidationError: If any validation rule is violated.

        Returns:
            dict: The same data dictionary passed as input if validation passes.
        """
        request_user_id = request_user.id
        users_to_add = data.get('users_to_add', [])
        users_to_exclude = data.get('users_to_exclude', [])

        users_to_add_ids = {u.id if hasattr(u, "id") else u for u in users_to_add}
        users_to_exclude_ids = {u.id if hasattr(u, "id") else u for u in users_to_exclude}

        if request_user_id in users_to_add_ids or request_user_id in users_to_exclude_ids:
            raise serializers.ValidationError(
                {
                    "detail": "You cannot add or exclude yourself because you are the owner."
                }
            )

        overlap = users_to_add_ids & users_to_exclude_ids

        if overlap:
            raise serializers.ValidationError(
                {
                    "detail": "A user cannot be both added and excluded in the same request."
                }
            )

        current_users = set(
            UserProject.objects.filter(project=proyectInstance)
            .values_list('user_id', flat=True)
        )
        already_in_project = users_to_add_ids & current_users

        if already_in_project:
            raise serializers.ValidationError(
                {
                    "detail": "These users are already part of the "
                    f"project: {list(already_in_project)}"
                }
            )

        invalid_excludes = users_to_exclude_ids - current_users

        if invalid_excludes:
            raise serializers.ValidationError(
                {
                    "detail": "Cannot exclude users that are not part of the "
                    f"project: {list(invalid_excludes)}"
                }
            )

        max_users = request_user.plan_type.max_users
        final_users_count = len((current_users - users_to_exclude_ids) | users_to_add_ids)

        if final_users_count > max_users:
            raise serializers.ValidationError(
                {
                    "detail": (
                        f"You cannot have more than {max_users} users in a project, "
                        "including yourself according to your plan."
                    )
                }
            )

        return data
