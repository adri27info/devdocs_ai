from utils.exceptions.instance.instance_exceptions import (
    InstanceInvalidValueException,
    InstanceUnexpectedValueException
)

from utils.general_utils import GeneralUtils


class UserBucketAttachmentValidator:
    """
    Service to validate user image attachments before processing.
    """

    __CHECK_ALREADY_PROCESSED = True

    def __init__(self, *, check_already_processed=None):
        """
        Initializes the service with option to check if attachment is already processed.

        Args:
            check_already_processed (bool, optional): Whether to check if attachment is
                already processed. Defaults True.
        """
        self.check_already_processed = GeneralUtils.use_default_if_none(
            value=check_already_processed,
            default=self.__CHECK_ALREADY_PROCESSED
        )

    def run(
        self,
        *,
        instance,
        user_image_bucket_url,
        aws_media_location,
    ):
        """
        Validates the attachment instance against various rules.

        Args:
            instance (Model): User model instance with attachment field.
            user_image_bucket_url (str): AWS S3 bucket URL for user images.
            aws_media_location (str): Base path for media files in AWS.

        Raises:
            InstanceUnexpectedValueException: If attachment was already processed
                or attachment name equals bucket URL.
            InstanceInvalidValueException: If AWS URLs are not set.
        """
        if self.check_already_processed and getattr(instance, '_attachment_processed', False):
            raise InstanceUnexpectedValueException("Attachment already processed.")

        if not user_image_bucket_url:
            raise InstanceInvalidValueException("AWS_USER_IMAGE_BUCKET_URL not set.")

        if not aws_media_location:
            raise InstanceInvalidValueException("AWS_MEDIA_LOCATION not set.")

        if instance.attachment.name == user_image_bucket_url:
            raise InstanceUnexpectedValueException(
                "Attachment name equals the bucket URL."
            )
