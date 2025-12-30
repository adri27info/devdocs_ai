from utils.cache.cache_max_limit_utils import CacheMaxLimitUtils
from utils.general_utils import GeneralUtils


class ResetPasswordAttemptsCacheInitService(CacheMaxLimitUtils):
    """
    Service to initialize and provide the maximum allowed reset-password attempts.
    """

    __MAX_RESET_PASSWORD_ATTEMPTS = 5

    def __init__(self, *, max_reset_password_attempts=None):
        """
        Initializes the service with a maximum number of reset-password attempts.

        Args:
            max_reset_password_attempts (int, optional): Maximum allowed attempts.
                Defaults to 5.
        """
        super().__init__(
            max_cache_limit=GeneralUtils.use_default_if_none(
                value=max_reset_password_attempts,
                default=self.__MAX_RESET_PASSWORD_ATTEMPTS
            )
        )

    def get_max_attempts(self):
        """
        Returns the maximum number of allowed reset-password attempts.

        Returns:
            int: Maximum reset-password attempts.
        """
        return self.get_max_limit()
