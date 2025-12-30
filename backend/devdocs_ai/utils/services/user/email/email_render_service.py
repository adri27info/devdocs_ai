from mjml.mjml2html import mjml_to_html

from django.template.loader import render_to_string

from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException


class EmailRenderService:
    """
    Service to render email templates into HTML for various email types.
    """

    __EMAIL_TEMPLATES = {
        "activation": "emails/activation_email.mjml",
        "resend_code_activation": "emails/resend_code_activation_email.mjml",
        "password_reset": "emails/password_reset_email.mjml",
        "password_reset_confirm": "emails/password_reset_confirm_email.mjml",
        "admin_assistance": "emails/admin_assistance.mjml",
        "project_invitation": "emails/project_invitation.mjml",
        "project_removed": "emails/project_removed.mjml",
        "project_deleted": "emails/project_deleted.mjml",
        "project_joined": "emails/project_joined.mjml",
        "attempts_resolved": "emails/attempts_resolved.mjml"
    }
    __DEFAULT_SUBJECTS = {
        "activation": "Activate your account",
        "resend_code_activation": "Your activation code",
        "password_reset": "Reset your password",
        "password_reset_confirm": "Your password has been changed",
        "admin_assistance": "Admin assistance request",
        "project_invitation": "New project invitation waiting for you",
        "project_removed": "You have been kicked",
        "project_deleted": "Project deleted",
        "project_joined": "A new user has joined your project",
        "attempts_resolved": "Attempts restored by admin"
    }
    __SUBJECTS = {
        "activation": __DEFAULT_SUBJECTS["activation"],
        "resend_code_activation": __DEFAULT_SUBJECTS["resend_code_activation"],
        "password_reset": __DEFAULT_SUBJECTS["password_reset"],
        "password_reset_confirm": __DEFAULT_SUBJECTS["password_reset_confirm"],
        "admin_assistance": __DEFAULT_SUBJECTS["admin_assistance"],
        "project_invitation": __DEFAULT_SUBJECTS["project_invitation"],
        "project_removed": __DEFAULT_SUBJECTS["project_removed"],
        "project_deleted": __DEFAULT_SUBJECTS["project_deleted"],
        "project_joined": __DEFAULT_SUBJECTS["project_joined"],
        "attempts_resolved": __DEFAULT_SUBJECTS["attempts_resolved"],
    }

    @classmethod
    def get_subject(cls, *, email_type):
        """
        Returns the email subject for a given email type.

        Args:
            email_type (str): Type of email.

        Returns:
            str: Subject line of the email.
        """
        return cls.__SUBJECTS.get(email_type, "No subject")

    @classmethod
    def run(cls, *, email_type, context):
        """
        Renders the email template for the specified type with given context.

        Args:
            email_type (str): Type of email.
            context (dict): Context dictionary to render template.

        Returns:
            str: Rendered HTML content.

        Raises:
            InstanceInvalidValueException: If template is not configured for type.
        """
        template_path = cls.__EMAIL_TEMPLATES.get(email_type)
        if not template_path:
            raise InstanceInvalidValueException(
                f"No template configured for '{email_type}'"
            )

        mjml_content = render_to_string(template_path, context)
        html_result = mjml_to_html(mjml_content)
        return html_result.html
