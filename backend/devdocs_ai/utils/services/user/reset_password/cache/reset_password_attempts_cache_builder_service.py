from utils.cache.cache_utils import CacheUtils


class ResetPasswordAttemptsCacheBuilderService:
    """
    Service to build cache keys for reset-password attempts.
    """

    @staticmethod
    def run(*, user_id):
        """
        Generates the cache key for a user's reset password attempts.

        Args:
            user_id (int): ID of the user.

        Returns:
            str: Cache key for reset password attempts.
        """
        return CacheUtils.build_cache_key(
            key="reset_password_attempts",
            value=user_id
        )
