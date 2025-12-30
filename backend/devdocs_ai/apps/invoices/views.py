from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.invoices.models import Invoice
from apps.invoices.serializers import InvoiceSerializer

from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.permissions.invoices.mixin import InvoiceAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.instace.instance_checker_service import InstanceCheckerService


class InvoiceView(
    CookieJWTAuthMixin,
    InvoiceAuthPermissionMixin,
    JSONParserMixin,
    GenericAPIView
):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    @validate_refresh_token(revoke=False)
    def get(self, request, *args, **kwargs):
        try:
            invoice = self.get_queryset().first()
            InstanceCheckerService.run(
                instance=invoice,
                message="Invoice not found."
            )
            serializer = self.get_serializer(instance=invoice)

            return Response(
                {
                    "message": "Invoice retrieved successfully.",
                    "invoice": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
