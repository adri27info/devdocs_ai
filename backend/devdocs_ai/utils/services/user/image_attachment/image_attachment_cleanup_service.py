import os

from utils.services.user.image_attachment.cache.image_attachment_cache_service import (
    ImageAttachmentCacheService
)


class ImageAttachmentCleanupService:
    """
    Service to prepare cleanup paths and clear attachment-related cache."""

    def __init__(self):
        pass

    def prepare_cleanup_path_and_clear_cache(
        self,
        *,
        aws_media_location,
        instance,
    ):
        """
        Clears attachment update count cache and prepares path for cleanup.

        Args:
            aws_media_location (str): Base AWS media path.
            instance (Model): User model instance with attachment field.

        Returns:
            str: Path to the directory for cleanup.
        """
        ImageAttachmentCacheService.delete_update_count_cache_key(
            user_id=instance.id
        )
        return f"{aws_media_location}{'/'.join(instance.attachment.name.split('/')[:-1])}/"

    def prepare_user_deletion_path(
        self,
        *,
        aws_media_location,
        instance
    ):
        """
        Prepares path to attachment directory for user deletion.

        Args:
            aws_media_location (str): Base AWS media path.
            instance (Model): User model instance with attachment field.

        Returns:
            str: Path to the user's attachment directory.
        """
        return f"{aws_media_location}{os.path.dirname(instance.attachment.name)}"
