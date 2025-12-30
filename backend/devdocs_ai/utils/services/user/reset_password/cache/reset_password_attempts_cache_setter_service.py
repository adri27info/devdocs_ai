from utils.cache.cache_max_limit_utils import CacheMaxLimitUtils
from utils.cache.cache_utils import CacheUtils

from utils.services.user.reset_password.cache.reset_password_attempts_cache_builder_service \
    import ResetPasswordAttemptsCacheBuilderService

from utils.services.user.reset_password.cache.reset_password_attempts_cache_init_service \
    import ResetPasswordAttemptsCacheInitService


class ResetPasswordAttemptsCacheSetterService(CacheMaxLimitUtils):
    """
    Service to set reset password attempts cache for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Sets the reset password attempts cache to the maximum allowed value.

        Args:
            user_id (int): ID of the user whose cache is being set.
        """
        CacheUtils.set_cache(
            key=ResetPasswordAttemptsCacheBuilderService.run(
                user_id=user_id
            ),
            value=ResetPasswordAttemptsCacheInitService().get_max_attempts()
        )
