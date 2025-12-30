from rest_framework import serializers

from apps.plans_types_formats.models import PlanTypeFormat


class PlanTypeFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanTypeFormat
        fields = "__all__"
