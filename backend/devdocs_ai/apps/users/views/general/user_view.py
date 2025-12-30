from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.users.models import User
from apps.users.serializers.general.user_serializer import (
    UserSerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer
)
from utils.decorators.methods.methods_decorators import validate_refresh_token
from utils.decorators.actions.actions_decorators import encapsule_refresh_decorator
from utils.mixins.auth.auth_mixins import CookieJWTAuthMixin
from utils.mixins.methods.methods_mixins import ExcludeHTTPMethodsMixin
from utils.mixins.parsers.parsers_mixins import FlexibleParserMixin
from utils.mixins.permissions.users.mixin import UserAuthPermissionMixin
from utils.services.response.response_handler_service import ResponseHandlerService


@encapsule_refresh_decorator(
    validate_refresh_token,
    revoke=False
)
class UserViewSet(
    CookieJWTAuthMixin,
    UserAuthPermissionMixin,
    ExcludeHTTPMethodsMixin,
    FlexibleParserMixin,
    ModelViewSet
):
    exclude_methods = [
        'post',
    ]

    def get_queryset(self):
        return User.objects.filter(is_active=True).exclude(role__name="admin")

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs["pk"], is_active=True)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        if self.action == 'change_password':
            return UserChangePasswordSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response(
            {
                "message": "Users listed successfully.",
                "users": {
                    "list": response.data
                }
            },
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response(
            {
                "message": "User retrieved successfully.",
                "user": response.data
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response(
            {
                "message": "User updated successfully.",
                "user": response.data
            },
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response = super().update(request, *args, **kwargs)

        return ResponseHandlerService.run(
            response=response,
            data={
                "message": "User updated successfully.",
                "user": response.data,
                "status_code": status.HTTP_200_OK,
            }
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response(
            {
                "message": "User deleted successfully."
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'], url_path='change-password')
    def change_password(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        return ResponseHandlerService.run(
            response=response,
            data={
                "message": "Password changed successfully.",
                "status_code": 200
            }
        )
