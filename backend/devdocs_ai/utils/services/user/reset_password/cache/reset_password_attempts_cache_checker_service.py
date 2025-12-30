from utils.cache.cache_utils import CacheUtils

from utils.services.user.reset_password.cache.reset_password_attempts_cache_builder_service \
    import ResetPasswordAttemptsCacheBuilderService

from utils.services.user.reset_password.cache.reset_password_attempts_cache_init_service \
    import ResetPasswordAttemptsCacheInitService


class ResetPasswordAttemptsCacheCheckerService:
    """
    Service to check if reset-password attempts have reached the maximum.
    """

    @staticmethod
    def run(*, user_id):
        """
        Checks if the user has exceeded the maximum reset password attempts.

        Args:
            user_id (int): ID of the user to check.

        Returns:
            bool: True if maximum attempts reached, False otherwise.
        """
        current = CacheUtils.get_cache(
            key=ResetPasswordAttemptsCacheBuilderService.run(
                user_id=user_id
            ),
        )

        return current == ResetPasswordAttemptsCacheInitService().get_max_attempts()
