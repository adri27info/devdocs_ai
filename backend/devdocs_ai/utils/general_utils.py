import random
import os
import uuid
import string

from django.conf import settings
from django.utils import timezone

from datetime import timedelta


class GeneralUtils:
    """
    General-purpose utility class for common application operations.
    """

    __ACTIVATION_CODE_LENGTH = 5
    __INVITATION_CODE_LENGTH = 12
    __INVITATION_CODE_EXPIRATION_DAYS_VALID = 1
    __BASE_EMAIL_CONTEXT = {"logo_url": settings.LOGO_URL}
    __BASE_FRONTEND_URL = settings.FRONTEND_URL.rstrip("/") + "/"
    __TITLE_CONTEXT_PROMPT = (
        "Analyze the following text.\n"
        "Provide a detailed documentation in plain text only.\n"
        "Do not include any formatting, HTML, or markdown.\n"
        "Text to document:\n"
    )

    @classmethod
    def get_title_context_prompt(cls):
        """
        Retrieves the base title context prompt string.

        Returns:
            str: A formatted string prompt for generating documentation titles.
        """
        return cls.__TITLE_CONTEXT_PROMPT

    @classmethod
    def generate_activation_code(cls):
        """
        Generates a numeric activation code of predefined length.

        Returns:
            str: A randomly generated numeric activation code as a string.
        """
        start = 10 ** (cls.__ACTIVATION_CODE_LENGTH - 1)
        end = (10 ** cls.__ACTIVATION_CODE_LENGTH) - 1
        return str(random.randint(start, end))

    @classmethod
    def generate_invitation_code(cls):
        """
        Generates a random invitation code consisting of uppercase letters and digits.

        Returns:
            str: A randomly generated invitation code.
        """
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=cls.__INVITATION_CODE_LENGTH))

    @classmethod
    def generate_invitation_code_expiration(cls):
        """
        Returns a datetime representing when an invitation code expires.

        Args:
            days_valid (int): Number of days the code is valid. Defaults to 1.

        Returns:
            datetime: Expiration datetime in UTC.
        """
        return timezone.now() + timedelta(
            days=cls.__INVITATION_CODE_EXPIRATION_DAYS_VALID
        )

    @classmethod
    def build_email_context(cls, **extra_context):
        """
        Builds a context dictionary for email templates.

        Args:
            **extra_context: Additional key-value pairs to include in the context.

        Returns:
            dict: Merged context containing base and additional values.
        """
        base_context = cls.__BASE_EMAIL_CONTEXT
        return {**base_context, **extra_context}

    @classmethod
    def build_frontend_url(cls, *, path=""):
        """
        Constructs a frontend URL based on the base frontend path.

        Args:
            path (str, optional): Additional path to append to the base frontend URL.
                Defaults to an empty string.

        Returns:
            str: The constructed frontend URL.
        """
        base_url = cls.__BASE_FRONTEND_URL
        return f"{base_url}{path.lstrip('/')}" if path else base_url

    @staticmethod
    def use_default_if_none(*, value, default):
        """
        Returns a default value if the provided value is None.

        Args:
            value (Any): Value to check for None.
            default (Any): Default value to use if `value` is None.

        Returns:
            Any: Either the provided value or the default.
        """
        return default if value is None else value

    @staticmethod
    def generate_attachment_path(
        *,
        instance,
        filename,
        folder="attachments",
        subfolder=None,
        use_user_pk=False,
        prefix=None
    ):
        """
        Generate a unique path for storing model attachments in a structured folder layout.

        The path format is: <folder>/<user_or_instance_id>/<subfolder>/<prefix>_<uuid>.<ext>
        This ensures uniqueness and avoids filename collisions. The user or instance must have
        a primary key.

        Args:
            instance (models.Model): The model instance that the file is associated with.
            filename (str): The original name of the uploaded file.
            folder (str): Base folder for storing attachments. Defaults to 'attachments'.
            subfolder (str, optional): Optional subfolder under the base folder.
            use_user_pk (bool): Use instance.user.pk instead of instance.pk if True.
                Defaults to False.
            prefix (str, optional): Optional prefix for the filename, e.g., 'invoice'.
                Defaults to None.

        Returns:
            str: A unique, structured file path for storing the uploaded file.
        """
        name, ext = os.path.splitext(filename)
        unique_id = uuid.uuid4().hex[:8]

        obj_id = instance.user.pk if use_user_pk else instance.pk
        unique_filename = f"{prefix}_{unique_id}{ext}" if prefix else f"{name}_{unique_id}{ext}"

        parts = [folder, str(obj_id)]

        if subfolder:
            parts.append(subfolder)

        parts.append(unique_filename)

        return os.path.join(*parts)
