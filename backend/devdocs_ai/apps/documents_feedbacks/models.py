from django.db import models


class DocumentFeedback(models.Model):
    document = models.ForeignKey(
        "documents.Document",
        related_name="documents_feedbacks",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    users = models.ManyToManyField(
        "users.User",
        related_name="users_documents_feedbacks",
        through="users_documents_feedbacks.UserDocumentFeedback"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Document feedback"
        verbose_name_plural = "Documents feedbacks"
