from utils.exceptions.instance.instance_exceptions import InstanceInternalErrorException
from utils.aws_utils import AWSUtils


class AWSS3BucketGetterService:
    """
    Service to provide a valid AWS S3 bucket instance.
    """

    @staticmethod
    def run():
        """
        Retrieves a valid S3 bucket instance.

        Raises:
            InstanceInternalErrorException: If the bucket is not found or configured.

        Returns:
            boto3.Bucket: The S3 bucket instance.
        """
        bucket = AWSUtils().get_bucket_s3()
        if not bucket:
            raise InstanceInternalErrorException(
                "S3 bucket not found or not configured."
            )
        return bucket
