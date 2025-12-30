from rest_framework.generics import GenericAPIView

from apps.plans_types_formats.models import PlanTypeFormat
from apps.plans_types_formats.serializers import PlanTypeFormatSerializer


class PlanTypeFormatView(GenericAPIView):
    serializer_class = PlanTypeFormatSerializer

    def get_queryset(self):
        return PlanTypeFormat.objects.all()
