from utils.general_utils import GeneralUtils


class CacheMaxLimitUtils:
    """
    Utility class for handling maximum cache limit configurations.
    """

    __MAX_CACHE_LIMIT = 1

    def __init__(self, max_cache_limit=None):
        """
        Initializes CacheMaxLimitUtils with a maximum cache limit.

        Args:
            max_cache_limit (int, optional): Maximum cache limit value. Defaults to 1.
        """
        self.max_cache_limit = GeneralUtils.use_default_if_none(
            value=max_cache_limit,
            default=self.__MAX_CACHE_LIMIT
        )

    def get_max_limit(self):
        """
        Retrieves the configured maximum cache limit.

        Returns:
            int: The maximum cache limit value.
        """
        return self.max_cache_limit
