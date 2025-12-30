from utils.cache.cache_max_limit_utils import CacheMaxLimitUtils
from utils.general_utils import GeneralUtils


class ActivationCodeExpirationCacheInitService(CacheMaxLimitUtils):
    """
    Service to provide the max expiration duration for activation code caches.
    """

    __MAX_ACTIVATION_CODE_EXPIRATION_MINUTES = 15

    def __init__(self, *, max_activation_code_expiration_minutes=None):
        super().__init__(
            max_cache_limit=GeneralUtils.use_default_if_none(
                value=max_activation_code_expiration_minutes,
                default=self.__MAX_ACTIVATION_CODE_EXPIRATION_MINUTES
            )
        )

    def get_max_expiration_minutes(self):
        """
        Returns the maximum expiration time in minutes for activation codes.

        Returns:
            int: Maximum expiration minutes.
        """
        return self.get_max_limit()
