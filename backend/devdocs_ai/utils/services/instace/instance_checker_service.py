from rest_framework.exceptions import NotFound


class InstanceCheckerService:
    """
    Service to verify the existence of an instance.
    """

    @staticmethod
    def run(*, instance, message="Instance not found."):
        """
        Check if the given instance exists and raise an exception if not.

        Args:
            instance (Any): The instance to validate.
            message (str, optional): Custom error message if instance is not found.
                Defaults to "Instance not found.".

        Raises:
            NotFound: If the instance is None, indicating the object does not exist.
        """
        if instance is None:
            raise NotFound(detail=message)
