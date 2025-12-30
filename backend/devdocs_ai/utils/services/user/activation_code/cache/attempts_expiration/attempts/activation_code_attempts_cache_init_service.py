from utils.cache.cache_max_limit_utils import CacheMaxLimitUtils
from utils.general_utils import GeneralUtils


class ActivationCodeAttemptsCacheInitService(CacheMaxLimitUtils):
    """
    Service to provide the max allowed activation code attempts for a user.
    """

    __MAX_ACTIVATION_CODE_ATTEMPTS = 5

    def __init__(self, *, max_activation_code_attempts=None):
        super().__init__(
            max_cache_limit=GeneralUtils.use_default_if_none(
                value=max_activation_code_attempts,
                default=self.__MAX_ACTIVATION_CODE_ATTEMPTS
            )
        )

    def get_max_attempts(self):
        """
        Returns the maximum allowed activation code attempts.

        Returns:
            int: Maximum activation code attempts.
        """
        return self.get_max_limit()
