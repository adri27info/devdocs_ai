from utils.cache.cache_rollback_utils import CacheRollbackUtils

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_setter_service \
    import ActivationCodeExpirationCacheSetterService


class ActivationCodeExpirationCacheExecutorService:
    """
    Service to execute setting of activation code expiration with rollback support.
    """

    def __init__(self):
        self.activation_code_expiration_setter = ActivationCodeExpirationCacheSetterService()

    def run(self, *, user_id):
        """
        Backs up current cache and sets new expiration for a user's activation code.

        Args:
            user_id (int): User ID whose cache will be updated.

        Returns:
            CacheRollbackUtils: Rollback object to restore previous cache if needed.
        """
        rollback = CacheRollbackUtils(
            key="activation_code_expiration",
            user_id=user_id
        )

        rollback.backup()

        self.activation_code_expiration_setter.run(
            user_id=user_id
        )

        return rollback
