from django.db import models

from utils.enums.choices_enums import NotificationTypeEnum
from utils.enums.choices_enums import ResetReasonEnum
from utils.enums.choices_enums import ActionRequiredReasonEnum


class Notification(models.Model):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    type = models.CharField(
        max_length=30,
        choices=NotificationTypeEnum.choices,
    )
    message_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    reset_reason = models.CharField(
        max_length=50,
        choices=ResetReasonEnum.choices,
        null=True,
        blank=True
    )
    action_required_reason = models.CharField(
        max_length=50,
        choices=ActionRequiredReasonEnum.choices,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
