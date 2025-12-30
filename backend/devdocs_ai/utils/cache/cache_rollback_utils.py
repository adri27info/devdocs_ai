from utils.cache.cache_utils import CacheUtils


class CacheRollbackUtils:
    """
    Utility class to backup and restore cache values for rollback operations.
    """

    def __init__(self, *, key, user_id):
        """
        Initializes CacheRollbackUtils with a cache key and user identifier.

        Args:
            key (str): Cache key template identifier.
            user_id (int or str): The user ID used to format the cache key.
        """
        self.key = key
        self.user_id = user_id
        self.previous_value = None

    def backup(self):
        """
        Backs up the current cache value before modification.

        Returns:
            Any: The cached value before the change, or None if not found.
        """
        cache_key = CacheUtils.build_cache_key(
            key=self.key,
            value=self.user_id
        )
        self.previous_value = CacheUtils.get_cache(key=cache_key)
        return self.previous_value

    def restore(self):
        """
        Restores the previously backed-up cache value.
        """
        if self.previous_value is not None:
            cache_key = CacheUtils.build_cache_key(
                key=self.key,
                value=self.user_id
            )
            CacheUtils.set_cache(key=cache_key, value=self.previous_value)
