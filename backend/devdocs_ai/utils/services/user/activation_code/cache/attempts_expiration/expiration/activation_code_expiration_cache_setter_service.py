from datetime import timedelta

from django.utils import timezone

from utils.cache.cache_utils import CacheUtils

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_builder_service \
    import ActivationCodeExpirationCacheBuilderService

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_init_service \
    import ActivationCodeExpirationCacheInitService


class ActivationCodeExpirationCacheSetterService:
    """
    Service to set the expiration timestamp for a user's activation code cache.
    """

    @staticmethod
    def run(*, user_id):
        """
        Sets the expiration timestamp for the activation code cache of a user.

        Args:
            user_id (int): User ID whose activation code expiration is set.
        """
        expires_at = timezone.now() + timedelta(
            minutes=ActivationCodeExpirationCacheInitService().get_max_expiration_minutes()
        )

        CacheUtils.set_cache(
            key=ActivationCodeExpirationCacheBuilderService.run(
                user_id=user_id
            ),
            value=int(expires_at.timestamp())
        )
