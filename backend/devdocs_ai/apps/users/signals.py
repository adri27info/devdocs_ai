from django.db.models.signals import (
    post_save,
    post_delete,
    pre_delete
)
from django.dispatch import receiver
from django.conf import settings

from apps.users.models import User
from apps.users_projects.models import UserProject
from apps.users.tasks import delete_files_s3

from utils.exceptions.instance.instance_exceptions import (
    InstanceNotFoundException,
    InstanceInvalidValueException,
    InstanceUnexpectedValueException
)
from utils.services.transaction.transaction_commit_executor_service import (
    TransactionCommitExecutorService
)
from utils.services.user.cache.user_cache_cleaner_service import UserCacheCleanupService
from utils.services.user.email.email_activation_checker_service import (
    EmailActivationCheckerService
)
from utils.services.user.email.email_service import EmailService
from utils.services.user.image_attachment.image_attachment_cleanup_service import (
    ImageAttachmentCleanupService
)
from utils.services.user.image_attachment.image_attachment_update_service import (
    ImageAttachmentUpdateService
)
from utils.validators.user.user_bucket_attachment_validator import UserBucketAttachmentValidator
from utils.general_utils import GeneralUtils
from utils.logger_utils import LoggerUtils


LOGGER = LoggerUtils().get_logger()
AWS_MEDIA_LOCATION = settings.AWS_MEDIA_LOCATION + "/"
USER_IMAGE_BUCKET_URL = settings.AWS_USER_IMAGE_BUCKET_URL


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Signal to send activation email after user creation.

    Sends email asynchronously only if user was created and should receive
    activation email. Runs after transaction commit.
    """
    def process_activation_email():
        try:
            should_send = EmailActivationCheckerService.run(
                instance=instance,
                created=created
            )
            if should_send:
                EmailService().send_email_task_async(
                    email_type="activation",
                    to_email=instance.email,
                    context=GeneralUtils.build_email_context(
                        user_email=instance.email,
                        activation_code=instance.activation_code,
                        activation_url=GeneralUtils.build_frontend_url(
                            path="activate-account"
                        )
                    )
                )
        except (
            InstanceNotFoundException,
            InstanceUnexpectedValueException
        ) as e:
            LOGGER.info(
                f"Activation email not sent for user {instance.email}: {e}"
            )
        except Exception as e:
            LOGGER.error(
                f"Failed to enqueue activation email for user {instance.email}: {e}"
            )

    TransactionCommitExecutorService.run(process_activation_email)


@receiver(post_save, sender=User)
def handle_user_image_attachment(sender, instance, created, **kwargs):
    """
    Signal to handle user image attachment after save.

    Updates or cleans up S3 attachments depending on whether the user was
    created or updated.
    """
    def process_attachment():
        try:
            imageAttachmentUpdateInstance = ImageAttachmentUpdateService()
            imageAttachmentValidationInstance = UserBucketAttachmentValidator()
            imageAttachmentCleanUpInstance = ImageAttachmentCleanupService()

            imageAttachmentValidationInstance.run(
                instance=instance,
                user_image_bucket_url=USER_IMAGE_BUCKET_URL,
                aws_media_location=AWS_MEDIA_LOCATION,
            )

            if created:
                imageAttachmentUpdateInstance.update_attachment_name(
                    aws_media_location=AWS_MEDIA_LOCATION,
                    instance=instance
                )
            else:
                if imageAttachmentUpdateInstance.should_trigger_cleanup(
                    instance=instance
                ):
                    path = imageAttachmentCleanUpInstance.prepare_cleanup_path_and_clear_cache(
                        aws_media_location=AWS_MEDIA_LOCATION,
                        instance=instance
                    )

                    delete_files_s3.delay(
                        user_folder_path=path,
                        operation_from="delete_oldest_files"
                    )
            instance._attachment_processed = True
            instance.save(update_fields=["attachment"])
        except (
            InstanceInvalidValueException,
            InstanceUnexpectedValueException
        ) as e:
            LOGGER.info(
                f"User {instance.id} attachment processing skipped: {e}"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error in handle_user_image_attachment signal: {e}"
            )

    TransactionCommitExecutorService.run(process_attachment)


@receiver(post_delete, sender=User)
def delete_user_image_attachment(sender, instance, **kwargs):
    """
    Signal to delete user image attachments on user deletion.

    Clears user caches and removes S3 files associated with the user's attachment.
    """
    try:
        UserCacheCleanupService.run(
            user_id=instance.id
        )

        imageAttachmentValidationInstance = UserBucketAttachmentValidator(
            check_already_processed=False
        )

        imageAttachmentValidationInstance.run(
            instance=instance,
            user_image_bucket_url=USER_IMAGE_BUCKET_URL,
            aws_media_location=AWS_MEDIA_LOCATION,
        )

        path = ImageAttachmentCleanupService().prepare_user_deletion_path(
            aws_media_location=AWS_MEDIA_LOCATION,
            instance=instance,
        )

        delete_files_s3.delay(
            user_folder_path=path,
            operation_from="delete_all",
        )
    except (
        InstanceInvalidValueException,
        InstanceUnexpectedValueException
    ) as e:
        LOGGER.info(
            f"User {instance.id} attachment processing skipped: {e}"
        )
    except Exception as e:
        LOGGER.error(
            f"Unexpected error in delete_user_image_attachment signal: {e}"
        )


@receiver(pre_delete, sender=User)
def delete_user_owned_projects(sender, instance, **kwargs):
    """
    Deletes projects where the deleted user was owner.
    Preserves projects where the user was only a member.
    """
    user_projects = UserProject.objects.filter(
        user=instance,
        role_project__name="owner"
    ).select_related('project')

    for up in user_projects:
        up.project.delete()
