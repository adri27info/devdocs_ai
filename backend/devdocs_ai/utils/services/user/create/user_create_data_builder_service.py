from utils.general_utils import GeneralUtils


class UserCreateDataBuilderService:
    """
    Service to build user creation data with plan, role, and activation code.
    """

    @staticmethod
    def run(*, plan, role, is_active, data):
        """
        Populates user creation data with plan, role, active status, and activation code.

        Args:
            plan (PlanType): User's plan type.
            role (Role): User's role.
            is_active (bool): Whether the user should be active.
            data (dict): Original user data dictionary to update.

        Returns:
            dict: Updated user creation data.
        """
        data["plan_type"] = plan
        data["role"] = role
        data["is_active"] = is_active
        data["activation_code"] = GeneralUtils.generate_activation_code()

        return data
