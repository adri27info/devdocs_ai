from io import BytesIO

from django.core.files.base import ContentFile, File

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from apps.documents.models import Document


class DocumentContextDocumentGeneratorService:
    """
    Service to generate TXT or PDF documents from text and save it to the model.

    Attributes:
        __BUFFER_START_POS (int): Initial buffer position for saving files.
        __PDF_PAGE_SIZE (tuple): Page size for PDF (default A4).
        __PDF_PARAGRAPH_STYLE (Style): ReportLab style for paragraphs.
        __PDF_SPACER_HEIGHT (int): Height of space between paragraphs.
    """
    __BUFFER_START_POS = 0
    __PDF_SPACER_HEIGHT = 12
    __PDF_PAGE_SIZE = A4
    __PDF_STYLES = getSampleStyleSheet()

    @classmethod
    def run(cls, *, document_context, generated_text, request_user):
        """
        Generate a document (TXT or PDF) from generated text and save it.

        Args:
            document_context (DocumentContext): Related document context instance.
            generated_text (str): Text content to include in the document.
            request_user (User): User who owns the document.

        Returns:
            Document: The created Document instance with the file saved.
        """
        if document_context.format.name == "plain":
            file_obj = ContentFile(generated_text.encode("utf-8"))
            file_obj.name = "document.txt"
        else:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=cls.__PDF_PAGE_SIZE)
            story = []

            for paragraph in generated_text.split("\n\n"):
                p = Paragraph(paragraph.replace("\n", "<br />"), cls.__PDF_STYLES['Normal'])
                story.append(p)
                story.append(Spacer(1, cls.__PDF_SPACER_HEIGHT))

            doc.build(story)
            buffer.seek(cls.__BUFFER_START_POS)
            file_obj = File(buffer, name="document.pdf")

        document = Document(
            user=request_user,
            document_context=document_context,
        )
        document.attachment.save(file_obj.name, file_obj, save=True)

        return document
