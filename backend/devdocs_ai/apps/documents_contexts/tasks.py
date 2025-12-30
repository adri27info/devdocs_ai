from celery import shared_task

from apps.documents_contexts.models import DocumentContext
from apps.users.models import User

from utils.services.document_context.document.document_context_document_generator_service import (
    DocumentContextDocumentGeneratorService
)


@shared_task()
def generate_document(*, document_context_id, generated_text, user_id):
    """
    Celery task to generate a TXT or PDF document asynchronously.

    This task retrieves the DocumentContext and User by their IDs, then delegates the
    creation of the document to DocumentContextDocumentGeneratorService. The generated
    file is saved to the Document model and uploaded to S3.

    Args:
        document_context_id (int): ID of the related DocumentContext instance.
        generated_text (str): Text content to include in the document.
        user_id (int): ID of the user who owns the document.
    """
    document_context = DocumentContext.objects.get(pk=document_context_id)
    user = User.objects.get(pk=user_id)

    DocumentContextDocumentGeneratorService.run(
        document_context=document_context,
        generated_text=generated_text,
        request_user=user,
    )
