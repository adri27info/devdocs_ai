from django.core.cache import cache

from apps.users.models import User

from utils.exceptions.instance.instance_exceptions import InstanceNotFoundException
from utils.services.user.activation_code.cache.general.activation_code_cache_reset_service \
    import ActivationCodeExpirationCacheResetService

from utils.services.user.image_attachment.cache.image_attachment_cache_service import (
    ImageAttachmentCacheService
)


class UserCreateCacheCleanerService:
    """
    Service to clean cached data of users that may not exist or were partially created.
    """

    __CACHE_KEY_PATTERN = "devdocs_ai:*"
    __MAX_RANGE_TO_SEARCH = 50

    @classmethod
    def cleanup_register_cache(cls):
        """
        Deletes cached activation codes and image attachment keys for missing users.

        It ensures only users with IDs higher than the last active user are cleaned.
        """
        last_active_user = User.objects.filter(is_active=True).order_by('-id').first()

        if not last_active_user:
            raise InstanceNotFoundException("Last user not found")

        last_active_id = last_active_user.id
        redis_client = cache.client.get_client()
        keys = redis_client.keys(cls.__CACHE_KEY_PATTERN)
        cached_ids = set(int(k.decode().split(":")[-1]) for k in keys)

        if not cached_ids:
            return

        pending_ids = [uid for uid in cached_ids if uid > last_active_id]

        if not pending_ids:
            return

        max_pending_id = max(pending_ids)

        for user_id in range(last_active_id + 1, max_pending_id + 1):
            cls._delete_user_cache(user_id=user_id)

        for user_id in range(max_pending_id + 1, max_pending_id + cls.__MAX_RANGE_TO_SEARCH):
            cls._delete_user_cache(user_id=user_id)

    @classmethod
    def _delete_user_cache(cls, *, user_id):
        """
        Deletes cached activation code and image attachment for a specific user.

        Args:
            user_id (int): ID of the user to delete cached data for.
        """
        ActivationCodeExpirationCacheResetService.run(
            user_id=user_id
        )
        ImageAttachmentCacheService.delete_name_and_count_cache_keys(
            user_id=user_id
        )
