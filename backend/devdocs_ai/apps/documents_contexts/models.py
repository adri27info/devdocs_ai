from django.db import models


class DocumentContext(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        related_name="documents_contexts",
        on_delete=models.CASCADE
    )
    format = models.ForeignKey(
        "formats.Format",
        related_name="documents_contexts",
        on_delete=models.CASCADE
    )
    llm = models.ForeignKey(
        "llms.LLM",
        related_name="documents_contexts",
        on_delete=models.CASCADE
    )
    body_prompt = models.TextField(
        max_length=15000,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Document context"
        verbose_name_plural = "Documents contexts"
