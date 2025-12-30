from rest_framework import serializers

from apps.roles_projects.models import RoleProject


class RoleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleProject
        fields = "__all__"
