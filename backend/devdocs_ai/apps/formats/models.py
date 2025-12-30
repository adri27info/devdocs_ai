from django.db import models

from utils.enums.choices_enums import DocumentationFormatEnum


class Format(models.Model):
    name = models.CharField(
        max_length=25,
        choices=DocumentationFormatEnum.choices,
        default=DocumentationFormatEnum.PLAIN
    )

    class Meta:
        verbose_name = "Format"
        verbose_name_plural = "Formats"
