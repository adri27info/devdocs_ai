from utils.cache.cache_utils import CacheUtils


class ActivationCodeAttemptsCacheBuilderService:
    """
    Service to build cache keys for activation code attempts."""

    @staticmethod
    def run(*, user_id):
        """
        Returns the cache key for a user's activation code attempts.

        Args:
            user_id (int): User ID to build cache key for.

        Returns:
            str: Full cache key for the user's activation code attempts.
        """
        return CacheUtils.build_cache_key(
            key="activation_code_attempts",
            value=user_id
        )
