from utils.cache.cache_utils import CacheUtils


class UserCacheCleanupService:
    """
    Service to clear all cached data related to a specific user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Deletes all cache keys associated with the given user ID.

        Args:
            user_id (int): ID of the user whose caches will be cleared.
        """
        for key_template in CacheUtils.get_all_cache_key_templates():
            cache_key = CacheUtils.build_cache_key(key=key_template, value=user_id)
            CacheUtils.delete_cache(key=cache_key)
