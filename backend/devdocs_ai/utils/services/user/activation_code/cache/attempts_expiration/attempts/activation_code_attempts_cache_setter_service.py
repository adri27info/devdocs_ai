from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_builder_service \
    import ActivationCodeAttemptsCacheBuilderService


class ActivationCodeAttemptsCacheSetterService:
    """
    Service to set or increment activation code attempts for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Sets or increments the activation code attempts cache for a user.

        If the cache exists, increment its value by 1. Otherwise, initialize it to 1.

        Args:
            user_id (int): User ID whose activation code attempts will be set.
        """
        cache_key = ActivationCodeAttemptsCacheBuilderService.run(
            user_id=user_id
        )

        if CacheUtils.get_cache(key=cache_key):
            CacheUtils.increment_cache_value(key=cache_key)
        else:
            CacheUtils.set_cache(key=cache_key, value=1)
