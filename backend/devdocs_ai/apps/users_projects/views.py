from rest_framework.generics import GenericAPIView

from apps.users_projects.models import UserProject
from apps.users_projects.serializers import UserProjectSerializer


class UserProjectView(GenericAPIView):
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        return UserProject.objects.all()
