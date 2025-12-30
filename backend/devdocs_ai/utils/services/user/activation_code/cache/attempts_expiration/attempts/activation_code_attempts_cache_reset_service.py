from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_builder_service \
    import ActivationCodeAttemptsCacheBuilderService


class ActivationCodeAttemptsCacheResetService:
    """
    Service to reset the activation code attempts cache for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Deletes the activation code attempts cache for the given user.

        Args:
            user_id (int): User ID whose activation code attempts cache is reset.
        """
        CacheUtils.delete_cache(
            key=ActivationCodeAttemptsCacheBuilderService.run(
                user_id=user_id
            )
        )
