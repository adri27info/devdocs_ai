from rest_framework import serializers

from apps.formats.models import Format


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = "__all__"
