from rest_framework import serializers

from apps.plans_types.models import PlanType
from apps.roles.models import Role

from utils.general_utils import GeneralUtils


class UserCreateValidator:
    """
    Validator for ensuring default plan and role exist when creating a user.
    """

    __PLAN_NAME = "free"
    __ROLE_NAME = "user"

    def __init__(self, *, plan_name=None, role_name=None):
        """
        Initializes the validator with optional plan and role names.

        Args:
            plan_name (str, optional): Name of the default plan. Defaults to 'free'.
            role_name (str, optional): Name of the default role. Defaults to 'user'.
        """
        self.plan_name = GeneralUtils.use_default_if_none(
            value=plan_name,
            default=self.__PLAN_NAME
        )
        self.role_name = GeneralUtils.use_default_if_none(
            value=role_name,
            default=self.__ROLE_NAME
        )

    def run(self):
        """
        Validates that default plan and role exist for user creation.

        Raises:
            serializers.ValidationError: If the default plan or role is missing.

        Returns:
            tuple: A tuple containing the default PlanType and Role instances.
        """
        default_plan = PlanType.objects.filter(name=self.plan_name).first()
        user_role = Role.objects.filter(name=self.role_name).first()

        if not default_plan:
            raise serializers.ValidationError(
                {
                    "detail": "When registering a user, the default plan must be assigned."
                }
            )

        if not user_role:
            raise serializers.ValidationError(
                {
                    "detail": "User role must exist in the system."
                }
            )

        return default_plan, user_role
