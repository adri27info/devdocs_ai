from django.db import models

from utils.general_utils import GeneralUtils


def document_attachment_upload_to(instance, filename):
    """
    Generate a unique file path for document attachments using GeneralUtils.
    """
    return GeneralUtils.generate_attachment_path(
        instance=instance,
        filename=filename,
        folder="attachments/user",
        subfolder="documents",
        use_user_pk=True,
        prefix="document"
    )


class Document(models.Model):
    attachment = models.FileField(
        upload_to=document_attachment_upload_to,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        "users.User",
        related_name="documents",
        on_delete=models.CASCADE
    )
    document_context = models.ForeignKey(
        "documents_contexts.DocumentContext",
        related_name="documents",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
