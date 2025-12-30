from django.db import models

from utils.general_utils import GeneralUtils


def invoice_attachment_upload_to(instance, filename):
    """
    Generate a unique file path for invoice attachments using GeneralUtils.
    """
    return GeneralUtils.generate_attachment_path(
        instance=instance,
        filename=filename,
        folder="attachments/user",
        subfolder="invoices",
        use_user_pk=True,
        prefix="invoice"
    )


class Invoice(models.Model):
    user = models.OneToOneField(
        "users.User",
        related_name="invoice",
        on_delete=models.CASCADE
    )
    plan_type = models.ForeignKey(
        "plans_types.PlanType",
        related_name="invoices",
        on_delete=models.CASCADE
    )
    attachment = models.FileField(
        upload_to=invoice_attachment_upload_to,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
