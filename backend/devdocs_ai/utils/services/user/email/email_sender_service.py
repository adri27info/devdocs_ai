from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class EmailSenderService:
    """
    Service to send raw emails with HTML content."""

    @staticmethod
    def run(*, subject, html, to_email):
        """
        Sends an email with the provided subject and HTML body.

        Args:
            subject (str): Email subject line.
            html (str): HTML content of the email.
            to_email (str): Recipient email address.
        """
        email = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [to_email])
        email.attach_alternative(html, "text/html")
        email.send()
