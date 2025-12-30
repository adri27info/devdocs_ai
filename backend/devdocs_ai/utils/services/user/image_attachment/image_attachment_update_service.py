from utils.services.user.image_attachment.cache.image_attachment_cache_service import (
    ImageAttachmentCacheService
)
from utils.general_utils import GeneralUtils


class ImageAttachmentUpdateService:
    """
    Service to track and update image attachment names and update counts.
    """

    __MAX_RENAMING_ATTACHMENT_UPDATES = 5

    def __init__(self, *, max_renaming_attachment_updates=None):
        """Initializes the service with maximum allowed renaming updates.

        Args:
            max_renaming_attachment_updates (int, optional): Max updates allowed.
                Defaults 5.
        """
        self.max_renaming_attachment_updates = GeneralUtils.use_default_if_none(
            value=max_renaming_attachment_updates,
            default=self.__MAX_RENAMING_ATTACHMENT_UPDATES
        )

    def should_trigger_cleanup(self, *, instance):
        """
        Determines if attachment renaming reached the max and triggers cleanup.

        Args:
            instance (Model): User model instance with attachment field.

        Returns:
            bool: True if max renaming reached and cleanup should occur.
        """
        cached_name = ImageAttachmentCacheService.get_name_cache_key_base(
            user_id=instance.id
        )
        cached_count = ImageAttachmentCacheService.get_update_count_cache_key_base(
            user_id=instance.id
        )

        if cached_name == instance.attachment.name:
            return False

        ImageAttachmentCacheService.set_name_cache_key(
            user_id=instance.id,
            attachment_name=instance.attachment.name
        )

        if cached_count:
            current_count = ImageAttachmentCacheService.increment_update_count_cache_key(
                user_id=instance.id
            )
        else:
            count = 1 if not cached_name else 2
            ImageAttachmentCacheService.set_update_count_cache_key(
                user_id=instance.id,
                count=count
            )
            current_count = count

        return current_count == self.max_renaming_attachment_updates

    def update_attachment_name(self, *, aws_media_location, instance):
        """
        Updates the cache with the current attachment name and returns full path.

        Args:
            aws_media_location (str): Base path for AWS media.
            instance (Model): User model instance with attachment field.

        Returns:
            str: Full path to the updated attachment.
        """
        ImageAttachmentCacheService.set_name_cache_key(
            user_id=instance.id,
            attachment_name=instance.attachment.name
        )

        return aws_media_location + instance.attachment.name
