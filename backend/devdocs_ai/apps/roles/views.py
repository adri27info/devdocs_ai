from rest_framework.generics import GenericAPIView

from apps.roles.models import Role
from apps.roles.serializers import RoleSerializer


class RoleView(GenericAPIView):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.all()
