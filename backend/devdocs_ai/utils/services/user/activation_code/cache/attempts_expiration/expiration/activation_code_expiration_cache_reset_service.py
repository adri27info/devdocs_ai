from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_builder_service \
    import ActivationCodeExpirationCacheBuilderService


class ActivationCodeExpirationCacheResetService:
    """
    Service to reset the activation code expiration cache for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Deletes the activation code expiration cache for the given user.

        Args:
            user_id (int): User ID whose cache will be reset.
        """
        CacheUtils.delete_cache(
            key=ActivationCodeExpirationCacheBuilderService.run(
                user_id=user_id
            )
        )
