from utils.cache.cache_utils import CacheUtils

from utils.services.user.reset_password.cache.reset_password_attempts_cache_builder_service \
    import ResetPasswordAttemptsCacheBuilderService


class ResetPasswordAttemptsCacheUpdaterService:
    """
    Service to increment or initialize the reset password attempts cache.
    """

    @staticmethod
    def run(*, user_id):
        """
        Increments reset password attempts count or initializes it to 1.

        Args:
            user_id (int): ID of the user whose attempts cache is updated.
        """
        cache_key = ResetPasswordAttemptsCacheBuilderService.run(
            user_id=user_id
        )

        if CacheUtils.get_cache(key=cache_key):
            CacheUtils.increment_cache_value(key=cache_key)
        else:
            CacheUtils.set_cache(key=cache_key, value=1)
