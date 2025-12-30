from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_reset_service \
    import ActivationCodeAttemptsCacheResetService

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_reset_service \
    import ActivationCodeExpirationCacheResetService


class ActivationCodeCacheResetService:
    """
    Service to reset user activation code-related caches.
    """

    __CACHES_TO_MANAGE = {
        "activation_code_attempts":
            ActivationCodeAttemptsCacheResetService.run,
        "activation_code_expiration":
            ActivationCodeExpirationCacheResetService.run
    }

    @classmethod
    def run(cls, *, user_id):
        """
        Resets all activation code-related cache keys for a user.

        Args:
            user_id (int): User ID for which caches will be reset.
        """
        for reset_service in cls.__CACHES_TO_MANAGE.values():
            reset_service(user_id=user_id)

    @classmethod
    def get_caches_to_manage(cls):
        """
        Returns a copy of all activation code caches managed by this service.

        Returns:
            dict: Cache name to reset function mapping.
        """
        return cls.__CACHES_TO_MANAGE.copy()
