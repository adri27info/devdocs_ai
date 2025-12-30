from rest_framework.generics import GenericAPIView

from apps.plans_types.models import PlanType
from apps.plans_types.serializers import PlanTypeSerializer


class PlanTypeView(GenericAPIView):
    serializer_class = PlanTypeSerializer

    def get_queryset(self):
        return PlanType.objects.all()
