import time
import boto3

from django.core.management.base import BaseCommand
from django.conf import settings

from utils.services.aws.ec2.aws_ec2_handler_service import AWSEC2HandlerService
from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class Command(BaseCommand):
    """
    Start or stop EC2 instance and manage Docker container
    """
    MAX_RETRIES_RUNNING = 15
    DELAY_RUNNING = 5
    MAX_RETRIES_PUBLIC_IP = 15
    DELAY_PUBLIC_IP = 5
    MAX_RETRIES_SSM = 5
    DELAY_SSM = 5
    SLEEP_BEFORE_SSM = 10
    CONTAINER_NAME = "fastapi-llm"

    def add_arguments(self, parser):
        """
        Add command line arguments for operation.
        """
        parser.add_argument(
            "operation",
            choices=["start", "stop"],
            help="Operation to perform on the EC2 instance",
        )

    def handle(self, *args, **options):
        """
        Handle the management command.
        """
        instance_id = getattr(settings, "EC2_INSTANCE_ID", None)
        region = getattr(settings, "AWS_DEFAULT_REGION", None)

        if not instance_id or not region:
            LOGGER.error("EC2_INSTANCE_ID or AWS_REGION not set in settings")
            return

        operation = options["operation"]

        if operation == "start":
            self.start_instance(instance_id, region)
        elif operation == "stop":
            self.stop_instance(instance_id, region)

    def start_instance(self, instance_id, region):
        """
        Start EC2 instance, wait until running and setup container

        Args:
            instance_id (str): EC2 instance ID.
            region (str): AWS region.
        """
        if not AWSEC2HandlerService.manage_service(
            operation="start",
            instance_id=instance_id
        ):
            LOGGER.error(f"Failed to start EC2 instance {instance_id}")
            return

        LOGGER.info(f"EC2 instance {instance_id} started successfully")

        if not self.wait_until_running(
            instance_id,
            self.MAX_RETRIES_RUNNING,
            self.DELAY_RUNNING
        ):
            LOGGER.error(f"EC2 instance {instance_id} did not reach running state in time")
            return

        public_ip = self.wait_for_public_ip(
            instance_id,
            self.MAX_RETRIES_PUBLIC_IP,
            self.DELAY_PUBLIC_IP
        )

        if public_ip:
            self.run_ssm_start_container(instance_id, region)
        else:
            LOGGER.warning("No public IP found for EC2 instance")

    def stop_instance(self, instance_id, region):
        """
        Stop Docker container inside EC2 and then stop the instance.

        Args:
            instance_id (str): EC2 instance ID.
            region (str): AWS region.
        """
        LOGGER.info(f"Stopping EC2 instance {instance_id}...")
        self.run_ssm_stop_container(instance_id, region)

        if not AWSEC2HandlerService.manage_service(
            operation="stop",
            instance_id=instance_id
        ):
            LOGGER.error(f"Failed to stop EC2 instance {instance_id}")
        else:
            LOGGER.info(f"EC2 instance {instance_id} stopped successfully")

    def wait_until_running(self, instance_id, retries, delay):
        """
        Wait until the EC2 instance is in 'running' state.

        Args:
            instance_id (str): EC2 instance ID.
            retries (int): Number of attempts.
            delay (int): Delay between attempts in seconds.

        Returns:
            bool: True if instance is running, False otherwise.
        """
        for attempt in range(retries):
            state = AWSEC2HandlerService.get_instance_state(
                instance_id=instance_id
            )

            if state == "running":
                LOGGER.info(f"EC2 instance {instance_id} is running")
                return True

            LOGGER.info(f"Waiting for instance to be running... attempt {attempt+1}/{retries}")
            time.sleep(delay)

        return False

    def wait_for_public_ip(self, instance_id, retries, delay):
        """
        Wait until the EC2 instance has a public IP.

        Args:
            instance_id (str): EC2 instance ID.
            retries (int): Number of attempts.
            delay (int): Delay between attempts in seconds.

        Returns:
            str or None: Public IP address if available, else None.
        """
        for attempt in range(retries):
            public_ip = AWSEC2HandlerService.get_public_ip(
                instance_id=instance_id
            )

            if public_ip:
                LOGGER.info(f"Public IP for instance {instance_id}: {public_ip}")
                return public_ip

            LOGGER.info(f"Waiting for public IP... attempt {attempt+1}/{retries}")
            time.sleep(delay)

        return None

    def run_ssm_stop_container(self, instance_id, region):
        """
        Stop and remove the Docker container inside EC2.

        Args:
            instance_id (str): EC2 instance ID.
            region (str): AWS region.
        """
        ssm_client = boto3.client("ssm", region_name=region)

        commands = (
            # Stop and remove Docker container if running
            f'CONTAINER=$(sudo docker ps -aq -f name={self.CONTAINER_NAME}); '
            f'if [ -n "$CONTAINER" ]; then '
            f'echo "Stopping container $CONTAINER..."; '
            f'sudo docker stop $CONTAINER || true; '
            f'sudo docker rm -f $CONTAINER || true; '
            f'else echo "No container named {self.CONTAINER_NAME} found"; fi'
        )

        response = ssm_client.send_command(
            DocumentName="AWS-RunShellScript",
            Targets=[{"Key": "InstanceIds", "Values": [instance_id]}],
            Parameters={"commands": [commands]},
        )

        LOGGER.info(
            f"Stop container command sent to instance {instance_id}, "
            f"Command ID: {response['Command']['CommandId']}"
        )

    def run_ssm_start_container(self, instance_id, region):
        """
        Start Docker container inside EC2, install Docker if needed, and create .env.

        Args:
            instance_id (str): EC2 instance ID.
            region (str): AWS region.
        """
        ssm_client = boto3.client("ssm", region_name=region)

        openrouter_api_key = getattr(settings, "OPENROUTER_API_KEY", None)
        openrouter_base_url = getattr(settings, "OPENROUTER_BASE_URL", None)
        openrouter_model = getattr(settings, "OPENROUTER_MODEL", None)
        image_ghcr = getattr(settings, "IMAGE_GHCR", None)

        if not all([
            openrouter_api_key,
            openrouter_base_url,
            openrouter_model,
            image_ghcr
        ]):
            LOGGER.error("OpenRouter settings or image GHCR not set in settings")
            return

        commands = (
            # Update system packages
            "sudo apt update && sudo apt upgrade -y",

            # Install Docker if not present (idempotent)
            (
                "if ! command -v docker &> /dev/null; then "
                "curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh; "
                "else echo 'Docker already installed, skipping installation'; fi"
            ),

            # Add ubuntu user to docker group (idempotent)
            "sudo usermod -aG docker ubuntu || true",

            # Install and start SSM agent if not running
            (
                "if ! systemctl is-active --quiet snap.amazon-ssm-agent.amazon-ssm-agent; then "
                "sudo snap install amazon-ssm-agent --classic && "
                "sudo systemctl enable amazon-ssm-agent && "
                "sudo systemctl start amazon-ssm-agent; fi"
            ),

            # Wait for Docker daemon to be ready
            (
                "for i in {1..10}; do "
                "if sudo docker info >/dev/null 2>&1; then break; fi; "
                "echo 'Waiting for Docker daemon...'; sleep 2; done"
            ),

            # Pull the latest image from GHCR
            f"sudo docker pull {image_ghcr}",

            # Create .env file with OpenRouter settings
            "cat <<EOT > /home/ubuntu/.env",
            f'OPENROUTER_API_KEY={openrouter_api_key}',
            f'OPENROUTER_BASE_URL={openrouter_base_url}',
            f'OPENROUTER_MODEL={openrouter_model}',
            "EOT",

            # Remove existing container if running and start new one
            (
                f"if [ $(sudo docker ps -aq -f name={self.CONTAINER_NAME}) ]; then "
                f"sudo docker rm -f $(sudo docker ps -aq -f name={self.CONTAINER_NAME}); fi"
            ),

            # Run the Docker container
            (
                f"sudo docker run -d -p 9000:9000 --name {self.CONTAINER_NAME} "
                "--env-file /home/ubuntu/.env "
                f"{image_ghcr}"
            ),
        )

        time.sleep(self.SLEEP_BEFORE_SSM)

        for attempt in range(self.MAX_RETRIES_SSM):
            try:
                response = ssm_client.send_command(
                    DocumentName="AWS-RunShellScript",
                    Targets=[{"Key": "InstanceIds", "Values": [instance_id]}],
                    Parameters={"commands": commands, "executionTimeout": ["3600"]},
                )
                LOGGER.info(
                    f"SSM command sent to instance {instance_id}, "
                    f"Command ID: {response['Command']['CommandId']}"
                )
                break
            except Exception:
                LOGGER.warning(
                    f"SSM agent not ready, retrying... attempt "
                    f"{attempt+1}/{self.MAX_RETRIES_SSM}"
                )
                time.sleep(self.DELAY_SSM)
        else:
            LOGGER.error(
                f"Failed to send SSM command to {instance_id} after "
                f"{self.MAX_RETRIES_SSM} attempts"
            )
