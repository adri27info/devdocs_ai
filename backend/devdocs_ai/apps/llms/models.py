from django.conf import settings
from django.db import models
from django.utils import timezone


class LLM(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(max_length=100)
    attachment = models.URLField(
        default=settings.LLM_URL,
    )
    max_tokens_per_request = models.PositiveIntegerField(default=5000)
    max_tokens_per_day = models.PositiveIntegerField(default=30000)
    tokens_per_day_used_today = models.PositiveIntegerField(default=0)
    tokens_per_day_last_reset = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LLM"
        verbose_name_plural = "LLMs"
