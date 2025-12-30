from django.db import models


class PlanTypeFormat(models.Model):
    plan_type = models.ForeignKey(
        "plans_types.PlanType",
        related_name="plans_types_formats",
        on_delete=models.CASCADE
    )
    format = models.ForeignKey(
        "formats.Format",
        related_name="plans_types_formats",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan type format"
        verbose_name_plural = "Plans types formats"
