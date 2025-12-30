from rest_framework import serializers

from apps.plans_types.models import PlanType


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = "__all__"
