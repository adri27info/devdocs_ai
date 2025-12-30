from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.documents_feedbacks.serializers import DocumentFeedbackCreateSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.documents_feedbacks.mixin import DocumentFeedbackAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)


class DocumentFeedbackView(
    CookieJWTAuthMixin,
    DocumentFeedbackAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = DocumentFeedbackCreateSerializer

    @validate_refresh_token(revoke=False)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            return Response(
                {
                    "message": "Vote generated successfully.",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
