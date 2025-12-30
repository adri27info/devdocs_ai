from django.db import models


class UserDocumentFeedback(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )
    document_feedback = models.ForeignKey(
        "documents_feedbacks.DocumentFeedback",
        on_delete=models.CASCADE
    )
    has_voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User document feedback"
        verbose_name_plural = "Users documents feedbacks"
