import re

from django.core.cache import cache


class CacheUtils:
    """
    Utility class for managing cache operations and key templates.
    """

    __CACHE_KEYS = {
        "user_attachment_name": "user_attachment_name:{user_id}",
        "user_attachment_update_count": "user_attachment_update_count:{user_id}",
        "activation_code_attempts": "activation_code_attempts:{user_id}",
        "activation_code_expiration": "activation_code_expiration:{user_id}",
        "reset_password_attempts": "reset_password_attempts:{user_id}",
    }

    @classmethod
    def get_all_cache_key_templates(cls):
        """
        Retrieves a copy of all cache key templates.

        Returns:
            dict: A dictionary of cache key templates.
        """
        return cls.__CACHE_KEYS.copy()

    @classmethod
    def increment_cache_value(cls, *, key):
        """
        Increments an integer cache value by one.

        Args:
            key (str): Cache key to increment.

        Returns:
            int or None: The new incremented value if successful; otherwise, None.
        """
        current_value = cls.get_cache(key=key)
        if isinstance(current_value, int):
            return cache.incr(key)

    @classmethod
    def build_cache_key(cls, *, key, value):
        """
        Builds a formatted cache key using a template and value.

        Args:
            key (str): Cache key template identifier.
            value (Any): Value to insert into the key template.

        Returns:
            str: The formatted cache key string.
        """
        pattern = cls.__CACHE_KEYS[key]
        return re.sub(r"\{[^}]+\}", str(value), pattern)

    @staticmethod
    def get_cache(*, key):
        """
        Retrieves a value from the cache.

        Args:
            key (str): Cache key to fetch.

        Returns:
            Any: The cached value or None if not found.
        """
        return cache.get(key)

    @staticmethod
    def set_cache(*, key, value, timeout=None):
        """
        Sets a value in the cache.

        Args:
            key (str): Cache key to store the value under.
            value (Any): Value to cache.
            timeout (int, optional): Expiration time in seconds. Defaults to None.
        """
        cache.set(key, value, timeout)

    @staticmethod
    def delete_cache(*, key):
        """
        Deletes a cache entry by key.

        Args:
            key (str): Cache key to remove.

        Returns:
            int: The number of keys deleted (1 if successful, 0 if not found).
        """
        return cache.delete(key)
