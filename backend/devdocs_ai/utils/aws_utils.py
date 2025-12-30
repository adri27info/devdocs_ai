import boto3

from django.conf import settings

from utils.general_utils import GeneralUtils


class AWSUtils:
    """
    Utility class for AWS service configuration and S3 resource handling.
    """

    __AWS_ACCESS_KEY_ID = getattr(settings, "AWS_ACCESS_KEY_ID", None)
    __AWS_SECRET_ACCESS_KEY = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
    __AWS_DEFAULT_REGION = getattr(settings, "AWS_DEFAULT_REGION", None)
    __AWS_STORAGE_BUCKET_NAME = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
    __USE_S3 = settings.USE_S3
    __SERVICE_NAME = "s3"

    def __init__(self, *, service_name=None):
        """
        Initializes AWSUtils with an optional service name.

        Args:
            service_name (str, optional): AWS service name to connect to.
            Defaults to 's3'.
        """
        self.service_name = GeneralUtils.use_default_if_none(
            value=service_name,
            default=self.__SERVICE_NAME
        )

    def build_resource(self):
        """
        Creates a boto3 resource instance for the configured AWS service.

        Returns:
            boto3.resources.base.ServiceResource: A boto3 service resource instance.
        """
        return boto3.resource(
            self.service_name,
            aws_access_key_id=self.__AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.__AWS_SECRET_ACCESS_KEY,
            region_name=self.__AWS_DEFAULT_REGION,
        )

    def build_client(self):
        """
        Creates a boto3 client instance for the configured AWS service.

        Returns:
            boto3.client: A boto3 client instance.
        """
        return boto3.client(
            self.service_name,
            aws_access_key_id=self.__AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.__AWS_SECRET_ACCESS_KEY,
            region_name=self.__AWS_DEFAULT_REGION,
        )

    def get_bucket_s3(self):
        """
        Retrieves the configured S3 bucket resource.

        Returns:
            boto3.resources.factory.s3.Bucket or None: The S3 bucket resource if S3
            usage is enabled; otherwise, None.
        """
        if not self.__USE_S3:
            return None
        return self.build_resource().Bucket(self.__AWS_STORAGE_BUCKET_NAME)
