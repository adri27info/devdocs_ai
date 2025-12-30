from celery import shared_task

from utils.services.aws.cloudfront.aws_cloudfront_invalidation_service import (
    AWSCloudFrontInvalidationService
)
from utils.services.aws.s3.aws_s3_bucket_getter_service import AWSS3BucketGetterService
from utils.services.aws.s3.aws_s3_file_deletion_service import AWSS3FileDeletionService
from utils.services.exception.exception_logger_handler_service import (
    ExceptionLoggerHandlerService
)
from utils.services.user.email.email_render_service import EmailRenderService
from utils.services.user.email.email_sender_service import EmailSenderService

from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


@shared_task
def send_email(*, email_type, to_email, context, raise_exception=False):
    """
    Asynchronous task to send an email.

    Args:
        email_type (str): Type of the email.
        to_email (str): Recipient email address.
        context (dict): Context data for rendering email template.
        raise_exception (bool, optional): Whether to raise exceptions. Defaults to False.
    """
    try:
        subject = EmailRenderService.get_subject(email_type=email_type)
        html = EmailRenderService.run(email_type=email_type, context=context)

        EmailSenderService.run(subject=subject, html=html, to_email=to_email)
        LOGGER.info(f"{email_type} email sent to {to_email}")
    except Exception as e:
        ExceptionLoggerHandlerService.run(
            message=f"Unexpected error sending {email_type} email to {to_email}. {e}",
            exc=e,
            raise_exception=raise_exception
        )


@shared_task
def delete_files_s3(*, user_folder_path, operation_from=None, raise_exception=False):
    """
    Asynchronous task to delete S3 files for a user folder.

    Optionally triggers CloudFront invalidation.

    Args:
        user_folder_path (str): S3 folder path to delete.
        operation_from (str, optional): Deletion operation type. Defaults to None.
        raise_exception (bool, optional): Raise exception if error occurs. Defaults to False.
    """
    try:
        bucket = AWSS3BucketGetterService.run()
        service = AWSS3FileDeletionService(bucket=bucket)

        invalidate_path = service.run(
            user_folder_path=user_folder_path,
            operation_from=operation_from
        )

        if invalidate_path:
            LOGGER.info(f"Invalidated CloudFront cache for: {invalidate_path}")
            invalidate_cloudfront_cache.delay(path=invalidate_path)
        else:
            LOGGER.info(f"No path to invalidate for {user_folder_path}")
    except Exception as e:
        ExceptionLoggerHandlerService.run(
            message=f"Error deleting files in prefix {user_folder_path}: {e}",
            exc=e,
            raise_exception=raise_exception
        )


@shared_task
def invalidate_cloudfront_cache(*, path, raise_exception=False):
    """
    Asynchronous task to invalidate CloudFront cache for given paths.

    Args:
        path (str or list): Path(s) to invalidate.
        raise_exception (bool, optional): Raise exception if error occurs. Defaults to False.
    """
    try:
        count = AWSCloudFrontInvalidationService.run(paths=path)
        LOGGER.info(f"CloudFront invalidation requested for {count} paths.")
    except Exception as e:
        ExceptionLoggerHandlerService.run(
            message=f"Error invalidating cloudfront cache: {e}",
            exc=e,
            raise_exception=raise_exception
        )
