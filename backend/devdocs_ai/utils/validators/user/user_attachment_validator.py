import mimetypes

from utils.validators.base.base_validator import BaseValidator


class UserAttachmentValidator(BaseValidator):
    """
    Validator to enforce file attachment rules including size and type.
    """

    def __init__(
        self,
        field_name="attachment",
        max_size_mb=5,
        allowed_types=None,
        error_key=None,
    ):
        """
        Initializes the attachment validator with constraints.

        Args:
            field_name (str): Name of the file field. Defaults to 'attachment'.
            max_size_mb (int): Maximum allowed file size in megabytes. Defaults to 5.
            allowed_types (list[str], optional): List of MIME types allowed.
                Defaults to ['image/jpeg', 'image/png'].
            error_key (str, optional): Custom key for error messages.
        """
        super().__init__(error_key=error_key)
        self.field_name = field_name
        self.max_size_mb = max_size_mb
        self.allowed_types = allowed_types or ["image/jpeg", "image/png"]

    def __call__(self, files):
        """
        Validates uploaded files against constraints.

        Args:
            files (MultiValueDict): Uploaded files from a request.

        Raises:
            ValidationError: If file count, size, or type violates constraints.
        """
        file_list = files.getlist(self.field_name)

        if len(file_list) > 1:
            self.raise_error(
                error_message="Only one attachment file is allowed."
            )

        if not file_list or not file_list[0]:
            return

        uploaded_file = file_list[0]

        if uploaded_file.size > self.max_size_mb * 1024 * 1024:
            self.raise_error(
                error_message=f"The file must not exceed {self.max_size_mb} MB."
            )

        mime_type, _ = mimetypes.guess_type(uploaded_file.name)

        if mime_type not in self.allowed_types:
            self.raise_error(
                error_message="Only JPG and PNG images are allowed."
            )
