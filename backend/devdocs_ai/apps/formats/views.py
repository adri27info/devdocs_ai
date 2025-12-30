from rest_framework.generics import GenericAPIView

from apps.formats.models import Format
from apps.formats.serializers import FormatSerializer


class FormatView(GenericAPIView):
    serializer_class = FormatSerializer

    def get_queryset(self):
        return Format.objects.all()
