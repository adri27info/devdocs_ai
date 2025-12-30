from utils.cache.cache_max_limit_utils import CacheMaxLimitUtils
from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_builder_service \
    import ActivationCodeAttemptsCacheBuilderService

from utils.services.user.activation_code.cache.attempts_expiration.\
    attempts.activation_code_attempts_cache_init_service \
    import ActivationCodeAttemptsCacheInitService


class ActivationCodeAttemptsCacheCheckerService(CacheMaxLimitUtils):
    """
    Service to check if a user has exceeded activation code attempts.
    """

    @staticmethod
    def run(*, user_id):
        """
        Checks if the user reached the max activation code attempts.

        Args:
            user_id (int): User ID to check attempts for.

        Returns:
            bool: True if max attempts reached, False otherwise.
        """
        current = CacheUtils.get_cache(
            key=ActivationCodeAttemptsCacheBuilderService.run(
                user_id=user_id
            )
        )

        return current == ActivationCodeAttemptsCacheInitService().get_max_attempts()
