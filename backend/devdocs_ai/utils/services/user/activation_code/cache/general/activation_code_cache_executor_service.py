from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.general.rollback.\
    activation_code_cache_rollback_service \
    import ActivationCodeCacheRollbackService

from utils.services.user.activation_code.cache.general.activation_code_cache_reset_service \
    import ActivationCodeCacheResetService


class ActivationCodeCacheExecutorService:
    """
    Service to execute activation code cache updates or restore previous state.
    """

    @staticmethod
    def run(*, user_id, pre_transaction_cache_values=None):
        """
        Executes cache updates or prepares rollbacks for activation code caches.

        If pre_transaction_cache_values is provided, sets missing cache values. Otherwise,
        backs up current cache values for later restoration.

        Args:
            user_id (int): User ID whose cache is managed.
            pre_transaction_cache_values (dict, optional): Pre-existing cache values to restore.

        Returns:
            dict or None: Rollback objects if no pre_transaction_cache_values provided.
        """
        caches_to_manage = ActivationCodeCacheResetService.get_caches_to_manage()

        if pre_transaction_cache_values is not None:
            for cache_key in caches_to_manage.keys():
                if cache_key == "activation_code_attempts":
                    continue

                full_key = CacheUtils.build_cache_key(key=cache_key, value=user_id)
                current_value = CacheUtils.get_cache(key=full_key)

                if not current_value:
                    CacheUtils.set_cache(
                        key=full_key,
                        value=pre_transaction_cache_values[cache_key]
                    )
        else:
            rollbacks = ActivationCodeCacheRollbackService.backup_cache_rollbacks(
                user_id=user_id
            )

            return rollbacks
