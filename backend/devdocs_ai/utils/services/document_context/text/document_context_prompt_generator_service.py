import requests

from django.conf import settings

from utils.exceptions.instance.instance_exceptions import InstanceUnexpectedValueException
from utils.services.aws.ec2.aws_ec2_handler_service import AWSEC2HandlerService


class DocumentContextPromptGeneratorService:
    """
    Service to generate documentation text using a FastAPI endpoint
    hosted on an EC2 instance.

    This service sends a prompt to the remote EC2-hosted FastAPI API and
    returns the generated text, automatically cleaning known markers such as
    [OST], [/OST], [OUT], [/OUT].

    Attributes:
        __EC2_INSTANCE_ID (str): EC2 instance ID retrieved from Django settings.
        __ENDPOINT_TIMEOUT (int): Timeout for HTTP requests in seconds.
        __MARKERS_TO_REMOVE (List[str]): List of markers to remove from the generated text.
    """

    __EC2_INSTANCE_ID = getattr(settings, "EC2_INSTANCE_ID", None)
    __ENDPOINT_TIMEOUT = 180
    __MARKERS_TO_REMOVE = [
        "[<s>]", "[</s>]", "<s>", "</s>",
        "[OST]", "[/OST]", "[OUT]", "[/OUT]"
    ]

    @classmethod
    def get_generated_text(cls, *, prompt: str) -> str:
        """
        Send a prompt to the EC2 FastAPI endpoint and return cleaned generated text.

        The method dynamically retrieves the EC2 public IP and sends the prompt
        to the FastAPI endpoint. Any predefined markers in the response are removed.

        Args:
            prompt (str): Input text prompt for documentation generation.

        Returns:
            str: Generated text with markers removed.

        Raises:
            InstanceUnexpectedValueException: If the EC2 instance ID is not set
                or the EC2 instance has no public IP.
            requests.HTTPError: If the HTTP request fails or returns an error status code.
        """
        if not cls.__EC2_INSTANCE_ID:
            raise InstanceUnexpectedValueException("EC2_INSTANCE_ID not set")

        public_ip = AWSEC2HandlerService.get_public_ip(
            instance_id=cls.__EC2_INSTANCE_ID
        )

        if not public_ip:
            raise InstanceUnexpectedValueException("EC2 instance has no public IP")

        response = requests.post(
            url=f"http://{public_ip}:9000/generate_text/",
            timeout=cls.__ENDPOINT_TIMEOUT,
            json={"prompt": prompt},
        )

        response.raise_for_status()
        raw_text = response.json().get("text", "")

        for marker in cls.__MARKERS_TO_REMOVE:
            raw_text = raw_text.replace(marker, "")

        return raw_text.strip()
