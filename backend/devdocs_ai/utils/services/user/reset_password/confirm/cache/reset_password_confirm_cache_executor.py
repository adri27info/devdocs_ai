from utils.cache.cache_rollback_utils import CacheRollbackUtils
from utils.cache.cache_utils import CacheUtils


class ResetPasswordConfirmCacheExecutorService:
    """
    Service to execute or rollback reset password cache operations.
    """

    @staticmethod
    def run(*, user_id, pre_transaction_cache_values=None):
        """
        Sets cache values for a user or creates a rollback object if none given.

        Args:
            user_id (int): ID of the user whose cache is being modified.
            pre_transaction_cache_values (dict, optional): Cache key-value pairs to set.

        Returns:
            CacheRollbackUtils: A rollback object if pre_transaction_cache_values is None.
        """
        if pre_transaction_cache_values is not None:
            for cache_key, value in pre_transaction_cache_values.items():
                full_key = CacheUtils.build_cache_key(key=cache_key, value=user_id)
                current_value = CacheUtils.get_cache(key=full_key)

                if current_value is None:
                    CacheUtils.set_cache(key=full_key, value=value)
        else:
            rollback = CacheRollbackUtils(
                key="reset_password_attempts",
                user_id=user_id
            )

            rollback.backup()

            return rollback
