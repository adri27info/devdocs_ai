from rest_framework import serializers

from apps.users_projects.models import UserProject


class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = "__all__"
