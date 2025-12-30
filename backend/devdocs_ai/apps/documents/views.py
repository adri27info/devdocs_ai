from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.documents.mixin import DocumentAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class DocumentView(
    CookieJWTAuthMixin,
    DocumentAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get("project_id")

        if project_id:
            queryset = Document.objects.filter(
                document_context__project__id=project_id,
                document_context__project__users=self.request.user
            ).distinct()
        else:
            queryset = Document.objects.filter(user=self.request.user)

        return queryset

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return Response(
                {
                    "message": "Documents listed successfully.",
                    "documents": {
                        "list": serializer.data
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
