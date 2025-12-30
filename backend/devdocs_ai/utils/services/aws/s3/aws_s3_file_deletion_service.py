from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.services.aws.s3.aws_s3_cleanup_service import AWSS3CleanupService
from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class AWSS3FileDeletionService:
    """
    Service to delete user files from an AWS S3 bucket.
    """

    __VALID_OPERATIONS = {"delete_all", "delete_oldest_files"}

    def __init__(self, *, bucket):
        """
        Initializes the file deletion service with a specific S3 bucket.

        Args:
            bucket (boto3.Bucket): The S3 bucket instance to operate on.
        """
        self.bucket = bucket

    def run(self, *, user_folder_path, operation_from):
        """
        Deletes files in the specified user folder based on the operation type.

        Args:
            user_folder_path (str): The path prefix for user's folder in S3.
            operation_from (str): Type of deletion ('delete_all' or 'delete_oldest_files').

        Raises:
            InstanceInvalidValueException: If the operation type is invalid.

        Returns:
            Union[str, list]: Deleted paths or string indicating all files deleted.
        """
        if operation_from not in self.__VALID_OPERATIONS:
            raise InstanceInvalidValueException(
                f"Invalid operation type: {operation_from}"
            )

        cleanup_service = AWSS3CleanupService(bucket=self.bucket)

        operation_methods = {
            "delete_all": cleanup_service.delete_all_files,
            "delete_oldest_files": cleanup_service.delete_oldest_files,
        }

        return operation_methods[operation_from](user_folder_path=user_folder_path)
