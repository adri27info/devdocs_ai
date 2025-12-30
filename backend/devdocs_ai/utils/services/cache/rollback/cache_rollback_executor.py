from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.services.exception.exception_response_service import ExceptionResponseHandlerService

from utils.services.user.activation_code.cache.attempts_expiration.expiration.\
    activation_code_expiration_cache_reset_service \
    import ActivationCodeExpirationCacheResetService

from utils.services.user.activation_code.cache.general.rollback.\
    activation_code_cache_rollback_service \
    import ActivationCodeCacheRollbackService

from utils.services.user.activation_code.cache.general.activation_code_cache_executor_service \
    import ActivationCodeCacheExecutorService

from utils.services.user.create.cache.user_create_cache_cleaner_service \
    import UserCreateCacheCleanerService

from utils.services.user.image_attachment.cache.image_attachment_cache_service \
    import ImageAttachmentCacheService

from utils.services.user.resend_activation_code.cache.resend_activation_code_cache_executor \
    import ResenActivationCodeCacheExecutorService

from utils.services.user.reset_password.confirm.cache.reset_password_confirm_cache_executor \
    import ResetPasswordConfirmCacheExecutorService


class CacheRollbackExecutorService:
    """
    Service to execute cache rollback or cleanup operations based on transaction results.
    """

    @staticmethod
    def run(
        *,
        instance=None,
        rollbacks=None,
        use_case=None,
        pre_transaction_cache_values=None
    ):
        """
        Execute cache operations after a transaction, either restoring previous state
        or cleaning up caches depending on success or failure.

        Args:
            instance (Any, optional): The instance related to the caches (usually a User).
            rollbacks (dict, optional): Rollback objects from pre-transaction caches.
            use_case (str): The current use case ('register', 'activate_account', etc.).
            pre_transaction_cache_values (dict, optional): Pre-transaction cache values.

        Returns:
            Response or None: If an exception occurs, returns a DRF Response with the error
            details.
        """
        try:
            if not use_case:
                raise InstanceInvalidValueException("Use case is invalid")

            caches_map = {
                "register": {
                    "on_success": {
                        "need_instance_id": True,
                        "funcs": (
                            ActivationCodeExpirationCacheResetService.run,
                            ImageAttachmentCacheService.delete_name_and_count_cache_keys,
                        )
                    },
                    "on_failed": {
                        "need_instance_id": False,
                        "funcs": (UserCreateCacheCleanerService.cleanup_register_cache,)
                    }
                },
                "activate_account": {
                    "on_success": {
                        "need_instance_id": False,
                        "funcs": (ActivationCodeCacheRollbackService.restore_rollbacks,)
                    },
                    "on_failed": {
                        "need_instance_id": True,
                        "funcs": (ActivationCodeCacheExecutorService.run,)
                    }
                },
                "resend_activation_code": {
                    "on_success": {
                        "need_instance_id": False,
                        "funcs": (ActivationCodeCacheRollbackService.restore_rollbacks,)
                    },
                    "on_failed": {
                        "need_instance_id": True,
                        "funcs": (ResenActivationCodeCacheExecutorService.run,)
                    }
                },
                "reset_password_confirm": {
                    "on_success": {
                        "need_instance_id": False,
                        "funcs": ("restore",)
                    },
                    "on_failed": {
                        "need_instance_id": True,
                        "funcs": (ResetPasswordConfirmCacheExecutorService.run,)
                    }
                },
                "reset_password": {
                    "on_success": {
                        "need_instance_id": False,
                        "funcs": ("restore",)
                    },
                    "on_failed": {
                        "need_instance_id": True,
                        "funcs": ()
                    }
                },
            }

            config_key = "on_success" if rollbacks else "on_failed"
            config = caches_map[use_case][config_key]

            for func in config["funcs"]:
                if isinstance(func, str):
                    if rollbacks:
                        method = getattr(rollbacks, func, None)
                        if callable(method):
                            method()
                else:
                    kwargs = {}

                    if config["need_instance_id"] and instance:
                        kwargs["user_id"] = instance.id

                    if rollbacks:
                        kwargs["rollbacks"] = rollbacks

                    if pre_transaction_cache_values:
                        kwargs["pre_transaction_cache_values"] = pre_transaction_cache_values

                    func(**kwargs)

        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
