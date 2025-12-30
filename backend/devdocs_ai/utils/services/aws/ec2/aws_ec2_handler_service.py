from django.conf import settings

from utils.aws_utils import AWSUtils


class AWSEC2HandlerService:
    """
    Service to handle AWS EC2 instance operations: start and stop instances.

    This class uses AWSUtils to build a boto3 client for EC2 and perform start or stop
    operations. It waits for the instance to reach the desired state before returning.

    Attributes:
        __SERVICE_NAME (str): AWS service name, default is 'ec2'.
        __EC2_STATUSES (dict): Mapping of logical statuses to boto3 waiter names.
    """
    __SERVICE_NAME = "ec2"
    __EC2_STATUSES = {
        "RUNNING": "instance_running",
        "STOPPED": "instance_stopped",
    }

    @classmethod
    def manage_service(cls, *, operation=None, instance_id=None):
        """
        Start or stop an EC2 instance and wait until it reaches the desired state.

        Args:
            operation (str): 'start' or 'stop' to control the instance.
            instance_id (str, optional): EC2 instance ID. Defaults to settings.EC2_INSTANCE_ID.

        Returns:
            bool: True if the operation succeeded, False otherwise.

        Notes:
            Exceptions are caught and return False on failure.
        """
        instance_id = instance_id or getattr(settings, "EC2_INSTANCE_ID", None)

        if not operation or not instance_id:
            return False

        aws_utils = AWSUtils(service_name=cls.__SERVICE_NAME)
        client = aws_utils.build_client()

        try:
            if operation == "start":
                client.start_instances(InstanceIds=[instance_id])
                waiter = client.get_waiter(cls.__EC2_STATUSES["RUNNING"])
                waiter.wait(InstanceIds=[instance_id])
                return True

            elif operation == "stop":
                client.stop_instances(InstanceIds=[instance_id])
                waiter = client.get_waiter(cls.__EC2_STATUSES["STOPPED"])
                waiter.wait(InstanceIds=[instance_id])
                return True

            return False
        except Exception as e:
            print(f"EC2 operation failed: {e}")
            return False

    @classmethod
    def get_public_ip(cls, *, instance_id=None):
        """
        Retrieve the public IP of an EC2 instance.

        Returns:
            str: Public IP or None if not available.
        """
        instance_id = instance_id or getattr(settings, "EC2_INSTANCE_ID", None)

        if not instance_id:
            return None

        aws_utils = AWSUtils(service_name=cls.__SERVICE_NAME)
        client = aws_utils.build_client()

        try:
            response = client.describe_instances(InstanceIds=[instance_id])
            reservations = response.get("Reservations", [])

            if not reservations:
                return None

            instances = reservations[0].get("Instances", [])

            if not instances:
                return None

            return instances[0].get("PublicIpAddress")
        except Exception as e:
            print(f"Failed to get public IP: {e}")
            return None

    @classmethod
    def get_instance_state(cls, *, instance_id=None):
        """
        Retrieve the current state of an EC2 instance.

        Args:
            instance_id (str, optional): EC2 instance ID. Defaults to
            settings.EC2_INSTANCE_ID.

        Returns:
            str | None: State name ('pending', 'running', 'stopping', 'stopped', etc.)
                or None if not available.
        """
        instance_id = instance_id or getattr(settings, "EC2_INSTANCE_ID", None)

        if not instance_id:
            return None

        aws_utils = AWSUtils(service_name=cls.__SERVICE_NAME)
        client = aws_utils.build_client()

        try:
            response = client.describe_instances(InstanceIds=[instance_id])
            reservations = response.get("Reservations", [])

            if not reservations:
                return None

            instances = reservations[0].get("Instances", [])

            if not instances:
                return None

            return instances[0].get("State", {}).get("Name")
        except Exception as e:
            print(f"Failed to get instance state: {e}")
            return None
