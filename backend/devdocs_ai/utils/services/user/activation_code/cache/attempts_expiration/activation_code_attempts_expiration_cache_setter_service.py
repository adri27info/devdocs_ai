from utils.services.user.activation_code.cache.attempts_expiration.attempts.\
    activation_code_attempts_cache_setter_service \
    import ActivationCodeAttemptsCacheSetterService

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_setter_service \
    import ActivationCodeExpirationCacheSetterService


class ActivationCodeAttemptsExpirationCacheSetterService:
    """
    Service to set both activation code attempts and expiration caches for a user.
    """

    @staticmethod
    def run(*, user_id):
        """
        Sets activation code attempts and expiration caches for a user.

        Args:
            user_id (int): User ID for whom the caches will be set.
        """
        ActivationCodeAttemptsCacheSetterService.run(
            user_id=user_id
        )

        ActivationCodeExpirationCacheSetterService.run(
            user_id=user_id
        )
