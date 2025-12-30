from utils.cache.cache_utils import CacheUtils

from utils.services.user.reset_password.cache.reset_password_attempts_cache_builder_service \
    import ResetPasswordAttemptsCacheBuilderService


class ResetPasswordAttemptsCacheResetService:
    """
    Service to reset reset-password attempts cache for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Deletes the reset password attempts cache for the specified user.

        Args:
            user_id (int): ID of the user whose cache is being deleted.
        """
        CacheUtils.delete_cache(
            key=ResetPasswordAttemptsCacheBuilderService.run(
                user_id=user_id
            ),
        )
