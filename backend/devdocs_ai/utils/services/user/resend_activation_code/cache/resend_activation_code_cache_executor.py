from utils.services.user.activation_code.cache.general.rollback.\
    activation_code_cache_rollback_service \
    import ActivationCodeCacheRollbackService


class ResenActivationCodeCacheExecutorService:
    """
    Service to execute cache rollback operations for resending activation codes.
    """

    @staticmethod
    def run(*, user_id):
        """
        Backs up and returns rollback objects for a user's activation code cache.

        Args:
            user_id (int): ID of the user whose activation code cache is being rolled back.

        Returns:
            list: List of rollback objects for the user's activation code cache.
        """
        rollbacks = ActivationCodeCacheRollbackService.backup_cache_rollbacks(
            user_id=user_id
        )

        return rollbacks
