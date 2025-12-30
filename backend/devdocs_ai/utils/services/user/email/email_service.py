from apps.users.tasks import send_email

from utils.general_utils import GeneralUtils


class EmailService:
    """
    Service to send emails asynchronously or synchronously.
    """

    __RAISE_EXCEPTION = True

    def __init__(self, *, raise_exception=None):
        """
        Initializes the email service with exception handling option.

        Args:
            raise_exception (bool, optional): Whether exceptions should be raised on
                synchronous sending. Defaults True.
        """
        self.raise_exception = GeneralUtils.use_default_if_none(
            value=raise_exception,
            default=self.__RAISE_EXCEPTION
        )

    def send_email_task_async(self, *, email_type, to_email, context):
        """
        Sends email asynchronously using a Celery task.

        Args:
            email_type (str): Type of email to send.
            to_email (str): Recipient email address.
            context (dict): Context dictionary for template rendering.

        Returns:
            AsyncResult: Celery task result.
        """
        return send_email.delay(
            email_type=email_type,
            to_email=to_email,
            context=context,
        )

    def send_email_task_sync(self, *, email_type, to_email, context):
        """
        Sends email synchronously.

        Args:
            email_type (str): Type of email to send.
            to_email (str): Recipient email address.
            context (dict): Context dictionary for template rendering.

        Returns:
            Any: Result of the synchronous send_email task.
        """
        return send_email.run(
            email_type=email_type,
            to_email=to_email,
            context=context,
            raise_exception=self.raise_exception
        )
