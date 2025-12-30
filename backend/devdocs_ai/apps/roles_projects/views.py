from rest_framework.generics import GenericAPIView

from apps.roles_projects.models import RoleProject
from apps.roles_projects.serializers import RoleProjectSerializer


class RoleProjectView(GenericAPIView):
    serializer_class = RoleProjectSerializer

    def get_queryset(self):
        return RoleProject.objects.all()
