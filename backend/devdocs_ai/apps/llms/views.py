
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.llms.models import LLM
from apps.llms.serializers import LLMSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.llms.mixin import LLMAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.instace.instance_checker_service import InstanceCheckerService


class LLMView(
    CookieJWTAuthMixin,
    LLMAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = LLMSerializer

    def get_queryset(self):
        return LLM.objects.all()

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        try:
            llm = self.get_queryset().first()
            InstanceCheckerService.run(
                instance=llm,
                message="LLM not found."
            )

            serializer = self.get_serializer(instance=llm)

            return Response(
                {
                    "message": "LLM model retrieved successfully.",
                    "llm": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
