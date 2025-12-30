from utils.cache.cache_rollback_utils import CacheRollbackUtils

from utils.services.user.activation_code.cache.general.activation_code_cache_reset_service \
    import ActivationCodeCacheResetService


class ActivationCodeCacheRollbackService:
    """
    Service to backup and restore activation code caches for a user.
    """

    @staticmethod
    def backup_cache_rollbacks(*, user_id):
        """
        Backs up current cache values for all activation code caches.

        Args:
            user_id (int): User ID whose caches will be backed up.

        Returns:
            dict: Mapping of cache key names to CacheRollbackUtils objects.
        """
        rollbacks = {}

        for key in ActivationCodeCacheResetService.get_caches_to_manage():
            rb = CacheRollbackUtils(key=key, user_id=user_id)
            rb.backup()
            rollbacks[key] = rb

        return rollbacks

    @staticmethod
    def restore_rollbacks(*, rollbacks):
        """
        Restores previously backed-up cache values for activation code caches.

        Args:
            rollbacks (dict): Mapping of cache key names to CacheRollbackUtils objects.
        """
        for rb in rollbacks.values():
            rb.restore()
