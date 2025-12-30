from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.documents_contexts.serializers import DocumentContextCreateSerializer
from apps.documents_contexts.tasks import generate_document

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.permissions.documents_contexts.mixin import DocumentContextAuthPermissionMixin
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin

from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.document_context.text.document_context_prompt_generator_service \
    import DocumentContextPromptGeneratorService

from utils.general_utils import GeneralUtils


class DocumentContextView(
    CookieJWTAuthMixin,
    DocumentContextAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = DocumentContextCreateSerializer

    @validate_refresh_token(revoke=False)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            doc_context = serializer.save()
            prompt = GeneralUtils.get_title_context_prompt() + doc_context.body_prompt

            generated_text = DocumentContextPromptGeneratorService.get_generated_text(
                prompt=prompt
            )

            generate_document.delay(
                document_context_id=doc_context.id,
                generated_text=generated_text,
                user_id=self.request.user.id
            )

            return Response(
                {
                    "message": "Documentation generated successfully.",
                    "generated_text": generated_text,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
