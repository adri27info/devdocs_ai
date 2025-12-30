from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.projects.filters import ProjectFilter
from apps.projects.models import Project
from apps.projects.serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    ProjectConfirmInvitationCodeSerializer,
    ProjectAddUserSerializer
)
from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.decorators.actions.actions_decorators import encapsule_refresh_decorator
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.methods.methods_mixins import ExcludeHTTPMethodsMixin
from utils.mixins.filters.filter_mixins import DjangoBaseFilterMixin
from utils.mixins.permissions.projects.mixin import ProjectAuthPermissionMixin
from utils.mixins.parsers.parsers_mixins import JSONParserMixin
from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)

from utils.services.project.add_user.project_add_user_handler_service \
    import ProjectAddUserHandlerService

from utils.services.project.confirm_invitation_code.\
    project_confirm_invitation_code_handler_service \
    import ProjectConfirmInvitationCodeHandlerService

from utils.services.project.create.project_create_handler_service \
    import ProjectCreateHandlerService

from utils.services.project.update.project_update_handler_service \
    import ProjectUpdateHandlerService

from utils.services.project.destroy.project_destroy_handler_service \
    import ProjectDestroyHandlerService

from utils.services.project.destroy.project_destroy_transaction_service \
    import ProjectDestroyTransactionService

from utils.services.transaction.transaction_executor_service import TransactionExecutorService


@encapsule_refresh_decorator(
    validate_refresh_token,
    revoke=False
)
class ProjectViewset(
    CookieJWTAuthMixin,
    ProjectAuthPermissionMixin,
    ExcludeHTTPMethodsMixin,
    JSONParserMixin,
    DjangoBaseFilterMixin,
    ModelViewSet
):
    filterset_class = ProjectFilter
    exclude_methods = ['patch']

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user).distinct()

    def get_serializer_class(self):
        if self.action == "create":
            return ProjectCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProjectUpdateSerializer
        elif self.action == "confirm_invitation_code":
            return ProjectConfirmInvitationCodeSerializer
        elif self.action == "add_user":
            return ProjectAddUserSerializer
        return ProjectSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response(
            {
                "message": "Projects listed successfully.",
                "projects": {
                    "list": response.data
                }
            },
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response(
            {
                "message": "Project retrieved successfully.",
                "project": response.data
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            TransactionExecutorService.run(
               db_ops=lambda: serializer.save()
            )

            ProjectCreateHandlerService.run(
                request_user=request.user,
                serializer=serializer
            )

            return Response(
                {
                    "message": "Project created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            TransactionExecutorService.run(
                db_ops=lambda: serializer.save()
            )

            ProjectUpdateHandlerService.run(
                serializer=serializer
            )

            return Response(
                {
                    "message": "Project updated successfully.",
                    "project": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            associated_users, _ = TransactionExecutorService.run(
                db_ops=lambda: ProjectDestroyTransactionService.run(
                    instance=instance,
                    request_user=request.user
                )
            )

            ProjectDestroyHandlerService.run(
                associated_users=associated_users,
                instance=instance,
                request_user=request.user
            )

            return Response(
                {
                    "message": "Project deleted successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)

    @action(detail=False, methods=['post'], url_path='confirm-invitation-code')
    def confirm_invitation_code(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            project, _ = TransactionExecutorService.run(
                db_ops=lambda: serializer.save()
            )
            owner = serializer.context.get("owner")

            ProjectConfirmInvitationCodeHandlerService.run(
                owner=owner,
                project=project
            )

            return Response(
                {
                    "message": "Invitation code validated successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)

    @action(detail=False, methods=['post'], url_path='add-user')
    def add_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            project, _ = TransactionExecutorService.run(
                db_ops=lambda: serializer.save()
            )
            user = serializer.validated_data["user"]

            ProjectAddUserHandlerService.run(
                user=user,
                project=project
            )

            return Response(
                {
                    "message": "User added successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return ExceptionResponseHandlerService.run(exc=e)
