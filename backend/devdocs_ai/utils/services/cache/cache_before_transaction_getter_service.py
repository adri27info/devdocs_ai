from utils.cache.cache_utils import CacheUtils


class CacheBeforeTransactionGetterService:
    """
    Service to fetch cache values before performing a transaction.
    """

    __CACHES_TO_MANAGE = {
        "activate_account_related": {
            "activation_code_expiration",
            "activation_code_attempts",
        },
        "reset_password_related": {
            "reset_password_attempts",
        },
    }

    @staticmethod
    def run(*, user_id, action):
        """
        Fetch current cache values for a given user and action.

        Args:
            user_id (int): ID of the user for whom to fetch cache values.
            action (str): Action name indicating which caches to fetch
                ('activate_account_related' or 'reset_password_related').

        Returns:
            dict: A dictionary mapping cache keys to their current values.
        """
        pre_transaction_values = {}

        for cache_key in CacheBeforeTransactionGetterService.__CACHES_TO_MANAGE[action]:
            full_key = CacheUtils.build_cache_key(key=cache_key, value=user_id)
            cached_value = CacheUtils.get_cache(key=full_key)
            pre_transaction_values[cache_key] = cached_value

        return pre_transaction_values
