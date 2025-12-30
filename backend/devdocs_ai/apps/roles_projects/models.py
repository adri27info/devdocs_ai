from django.db import models

from utils.enums.choices_enums import RoleProjectEnum


class RoleProject(models.Model):
    name = models.CharField(
        max_length=20,
        choices=RoleProjectEnum.choices,
        default=RoleProjectEnum.OWNER,
    )

    class Meta:
        verbose_name = "Role project"
        verbose_name_plural = "Roles projects"
