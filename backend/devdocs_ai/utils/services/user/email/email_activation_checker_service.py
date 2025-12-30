from apps.users.models import User

from utils.exceptions.instance.instance_exceptions import (
    InstanceNotFoundException,
    InstanceUnexpectedValueException
)


class EmailActivationCheckerService:
    """
    Service to determine if an activation email should be sent for a user.
    """

    __ROLE_ADMIN_NAME = "admin"

    @classmethod
    def run(cls, *, instance, created):
        """
        Checks conditions to decide if activation email should be sent.

        Args:
            instance (User): User instance.
            created (bool): True if the user was just created.

        Returns:
            bool: True if email should be sent, False otherwise.

        Raises:
            InstanceNotFoundException: If no admin user exists.
            InstanceUnexpectedValueException: If user email belongs to admin or is active.
        """
        if not created:
            return False

        admin = User.objects.filter(role__name=cls.__ROLE_ADMIN_NAME).first()

        if not admin:
            raise InstanceNotFoundException(
                "Admin user must be created to validate new user emails."
            )

        if instance.email == admin.email:
            raise InstanceUnexpectedValueException(
                "The email is not sent because it belongs to the admin user."
            )

        if instance.is_active:
            raise InstanceUnexpectedValueException(
                "The email is not sent because the user account is already active."
            )

        return True
