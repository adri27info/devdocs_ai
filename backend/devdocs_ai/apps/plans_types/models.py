from django.db import models

from utils.enums.choices_enums import SubscriptionPlanEnum


class PlanType(models.Model):
    name = models.CharField(
        max_length=50,
        choices=SubscriptionPlanEnum.choices,
        unique=True
    )
    max_projects = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()
    can_invite = models.BooleanField(default=False)
    is_private_allowed = models.BooleanField(default=False)
    formats = models.ManyToManyField(
        "formats.Format",
        related_name="plan_types",
        through="plans_types_formats.PlanTypeFormat",
    )

    class Meta:
        verbose_name = "Plan type"
        verbose_name_plural = "Plans types"
