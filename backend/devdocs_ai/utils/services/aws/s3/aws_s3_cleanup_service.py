import os

from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class AWSS3CleanupService:
    """
    Service to clean up files in a specified AWS S3 bucket.
    """

    __MAX_FILES_BEFORE_CLEANUP = 5

    def __init__(self, *, bucket):
        """
        Initializes the cleanup service with a specific S3 bucket.

        Args:
            bucket (boto3.Bucket): The S3 bucket instance to operate on.
        """
        self.bucket = bucket

    def delete_all_files(self, *, user_folder_path):
        """
        Deletes all files under a given user folder path.

        Args:
            user_folder_path (str): The S3 path prefix of the user folder.

        Raises:
            InstanceInvalidValueException: If no files are found.

        Returns:
            str: Path pattern representing deleted files.
        """
        files = list(self.bucket.objects.filter(Prefix=user_folder_path))

        if not files:
            raise InstanceInvalidValueException(
                f"No files found in {user_folder_path}"
            )

        delete_keys = [{"Key": file.key} for file in files]
        self.bucket.delete_objects(Delete={"Objects": delete_keys})
        LOGGER.info(f"All files deleted from: {user_folder_path}")
        return f"{user_folder_path}/*"

    def delete_oldest_files(self, *, user_folder_path):
        """
        Deletes oldest files in a user folder while preserving the latest.

        Args:
            user_folder_path (str): The S3 path prefix of the user folder.

        Raises:
            InstanceInvalidValueException: If file count does not match expected.
            InstanceInvalidValueException: If no files are found.

        Returns:
            list[str]: Paths of deleted files.
        """
        folder_prefix = os.path.dirname(user_folder_path)
        files = list(self.bucket.objects.filter(Prefix=folder_prefix))
        files = [
            f for f in files
            if not f.key.endswith("/")
            and f.key.split("/")[-1].startswith("user_")
        ]

        if not files:
            raise InstanceInvalidValueException(
                f"No files found in {user_folder_path}"
            )

        if len(files) != self.__MAX_FILES_BEFORE_CLEANUP:
            raise InstanceInvalidValueException(
                f"Skipping deletion. Found {len(files)} files in {folder_prefix}, "
                f"expected {self.__MAX_FILES_BEFORE_CLEANUP}."
            )

        files_sorted = sorted(files, key=lambda x: x.last_modified, reverse=True)
        files_to_delete = files_sorted[1:]
        delete_keys = [{"Key": file.key} for file in files_to_delete]
        paths_to_invalidate = [file.key for file in files_to_delete]

        self.bucket.delete_objects(Delete={"Objects": delete_keys})
        LOGGER.info(f"Old files deleted from {folder_prefix}, preserved latest.")
        return paths_to_invalidate
