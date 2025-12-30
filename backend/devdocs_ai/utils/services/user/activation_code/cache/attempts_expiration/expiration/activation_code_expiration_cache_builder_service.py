from utils.cache.cache_utils import CacheUtils


class ActivationCodeExpirationCacheBuilderService:
    """
    Service to build cache keys for activation code expiration.
    """

    @staticmethod
    def run(*, user_id):
        """
        Returns the cache key for a user's activation code expiration.

        Args:
            user_id (int): User ID to build the cache key for.

        Returns:
            str: Full cache key for the activation code expiration.
        """
        return CacheUtils.build_cache_key(
            key="activation_code_expiration",
            value=user_id
        )
