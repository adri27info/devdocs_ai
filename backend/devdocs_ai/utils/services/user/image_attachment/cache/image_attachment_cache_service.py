from utils.cache.cache_utils import CacheUtils


class ImageAttachmentCacheService:
    """
    Service to manage caching of attachment names and update counts."""

    @classmethod
    def get_name_cache_key_base(cls, *, user_id):
        """
        Gets cached attachment name for a user.

        Args:
            user_id (int): ID of the user.

        Returns:
            str | None: Cached attachment name.
        """
        return CacheUtils.get_cache(
            key=cls.get_name_cache_key(
                user_id=user_id
            )
        )

    @classmethod
    def get_update_count_cache_key_base(cls, *, user_id):
        """
        Gets cached update count for a user's attachment.

        Args:
            user_id (int): ID of the user.

        Returns:
            int | None: Cached update count.
        """
        return CacheUtils.get_cache(
            key=cls.get_update_count_cache_key(
                user_id=user_id
            )
        )

    @classmethod
    def increment_update_count_cache_key(cls, *, user_id):
        """
        Increments the update count in cache for a user's attachment.

        Args:
            user_id (int): ID of the user.

        Returns:
            int: New update count.
        """
        return CacheUtils.increment_cache_value(
            key=cls.get_update_count_cache_key(
                user_id=user_id
            )
        )

    @classmethod
    def delete_name_and_count_cache_keys(cls, *, user_id):
        """
        Deletes both attachment name and update count cache for a user.

        Args:
            user_id (int): ID of the user.
        """
        CacheUtils.delete_cache(
            key=cls.get_name_cache_key(
                user_id=user_id
            )
        )
        CacheUtils.delete_cache(
            key=cls.get_update_count_cache_key(
                user_id=user_id
            )
        )

    @classmethod
    def delete_update_count_cache_key(cls, *, user_id):
        """
        Deletes only the update count cache for a user's attachment.

        Args:
            user_id (int): ID of the user.
        """
        CacheUtils.delete_cache(
            key=cls.get_update_count_cache_key(
                user_id=user_id
            )
        )

    @classmethod
    def set_name_cache_key(cls, *, user_id, attachment_name):
        """
        Sets attachment name in cache for a user.

        Args:
            user_id (int): ID of the user.
            attachment_name (str): Name of the attachment to cache.
        """
        CacheUtils.set_cache(
            key=cls.get_name_cache_key(
                user_id=user_id
            ),
            value=attachment_name
        )

    @classmethod
    def set_update_count_cache_key(cls, *, user_id, count=1):
        """
        Sets update count in cache for a user's attachment.

        Args:
            user_id (int): ID of the user.
            count (int, optional): Count value. Defaults to 1.
        """
        CacheUtils.set_cache(
            key=cls.get_update_count_cache_key(
                user_id=user_id
            ),
            value=count
        )

    @staticmethod
    def get_name_cache_key(*, user_id):
        """
        Builds the cache key for a user's attachment name.

        Args:
            user_id (int): ID of the user.

        Returns:
            str: Cache key string.
        """
        return CacheUtils.build_cache_key(
            key="user_attachment_name",
            value=user_id
        )

    @staticmethod
    def get_update_count_cache_key(*, user_id):
        """
        Builds the cache key for a user's attachment update count.

        Args:
            user_id (int): ID of the user.

        Returns:
            str: Cache key string.
        """
        return CacheUtils.build_cache_key(
            key="user_attachment_update_count",
            value=user_id
        )
