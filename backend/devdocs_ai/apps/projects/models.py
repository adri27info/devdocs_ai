from django.db import models

from utils.enums.choices_enums import PrivacyEnum
from utils.general_utils import GeneralUtils


class Project(models.Model):
    name = models.CharField(max_length=35)
    description = models.CharField(max_length=255)
    privacy = models.CharField(
        max_length=25,
        choices=PrivacyEnum.choices,
    )
    invitation_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    invitation_code_expires_at = models.DateTimeField(
        default=GeneralUtils.generate_invitation_code_expiration
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
