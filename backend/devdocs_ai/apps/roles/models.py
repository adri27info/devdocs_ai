from django.db import models

from utils.enums.choices_enums import RoleEnum


class Role(models.Model):
    name = models.CharField(
        max_length=20,
        choices=RoleEnum.choices,
        default=RoleEnum.USER,
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
