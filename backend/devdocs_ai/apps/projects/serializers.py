from rest_framework import serializers

from apps.users.models import User
from apps.projects.models import Project
from apps.users_projects.models import UserProject
from apps.roles_projects.models import RoleProject
from apps.users.serializers.general.user_serializer import UserSerializer
from apps.roles_projects.serializers import RoleProjectSerializer

from utils.general_utils import GeneralUtils
from utils.exceptions.db.db_exceptions import DatabaseOperationException
from utils.services.project.create.project_create_executor_service import \
    ProjectCreateExecutorService

from utils.services.project.update.project_update_executor_service import \
    ProjectUpdateExecutorService

from utils.services.project.add_user.project_add_user_executor_service import \
    ProjectAddUserExecutorService

from utils.validators.project.add_user.project_add_user_validator import \
    ProjectAddUserValidator

from utils.validators.project.create.project_create_validator import \
    ProjectCreateValidator

from utils.validators.project.update.project_update_validator \
    import ProjectUpdateValidator

from utils.validators.project.confirm_invitation_code.project_confirm_invitation_code_validator \
    import ProjectConfirmInvitationCodeValidator

from utils.services.project.confirm_invitation_code.\
    project_confirm_invitation_code_executor_service \
    import ProjectConfirmInvitationCodeExecutorService


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = [
            "invitation_code",
            "invitation_code_expires_at"
        ]

    def get_users(self, obj):
        users_data = []

        user_projects = UserProject.objects.filter(
            project=obj
        ).select_related("user", "role_project")

        for up in user_projects:
            user_data = UserSerializer(up.user).data
            user_data["role_project"] = RoleProjectSerializer(up.role_project).data
            users_data.append(user_data)

        return users_data


class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        allow_empty=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'privacy',
            "users"
        ]
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'max_length': 'Name cannot exceed 35 characters.',
                    'required': 'Name is required.',
                    'blank': 'Name may not be blank.'
                }
            },
            'description': {
                'error_messages': {
                    'max_length': 'Description cannot exceed 255 characters.',
                    'required': 'Description is required.',
                    'blank': 'Description may not be blank.'
                }
            },
            'privacy': {
                'error_messages': {
                    'max_length': 'Privacy cannot exceed 25 characters.',
                    'required': 'Privacy is required.',
                    "invalid_choice": (
                        "Invalid privacy. Must be one of: 'public' or 'private'."
                    )
                }
            }
        }

    def validate(self, data):
        data = ProjectCreateValidator.run(
            request_user=self.context['request'].user,
            data=data,
        )

        return data

    def create(self, validated_data):
        try:
            project = ProjectCreateExecutorService.run(
                request_user=self.context['request'].user,
                validated_data=validated_data
            )

            return project
        except Exception:
            raise DatabaseOperationException(
                "Project could not be created."
            )


class ProjectUpdateSerializer(serializers.ModelSerializer):
    users_to_exclude = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        allow_empty=True,
        required=False
    )
    users_to_add = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        allow_empty=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'privacy',
            "users_to_exclude",
            "users_to_add",
        ]
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'max_length': 'Name cannot exceed 35 characters.',
                    'required': 'Name is required.',
                    'blank': 'Name may not be blank.'
                }
            },
            'description': {
                'error_messages': {
                    'max_length': 'Description cannot exceed 255 characters.',
                    'required': 'Description is required.',
                    'blank': 'Description may not be blank.'
                }
            },
            'privacy': {
                'error_messages': {
                    'max_length': 'Privacy cannot exceed 25 characters.',
                    'required': 'Privacy is required.',
                    "invalid_choice": (
                        "Invalid privacy. Must be one of: 'public' or 'private'."
                    )
                }
            }
        }

    def validate(self, data):
        data = ProjectUpdateValidator.run(
            request_user=self.context['request'].user,
            proyectInstance=self.instance,
            data=data
        )

        return data

    def update(self, instance, validated_data):
        try:
            request_user = self.context['request'].user
            validated_data["invitation_code"] = GeneralUtils.generate_invitation_code()
            project_update = super().update(instance, validated_data)

            ProjectUpdateExecutorService.run(
                request_user=request_user,
                instance=project_update,
                users_to_add=validated_data.get('users_to_add', []),
                users_to_exclude=validated_data.get('users_to_exclude', [])
            )

            return project_update
        except Exception:
            raise DatabaseOperationException(
                "Project could not be updated."
            )


class ProjectConfirmInvitationCodeSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(
        required=True,
        max_length=12,
        error_messages={
            'required': 'Invitation code is required.',
            'blank': 'Invitation code may not be blank.',
            'max_length': 'Invitation code cannot exceed 12 characters.',
        }
    )

    def validate_invitation_code(self, value):
        return value.strip().upper()

    def validate(self, data):
        invitation_code = data.get('invitation_code')
        request_user = self.context['request'].user

        data['project'] = ProjectConfirmInvitationCodeValidator.run(
            invitation_code=invitation_code,
            request_user=request_user
        )

        return data

    def create(self, validated_data):
        try:
            request_user = self.context['request'].user
            project = validated_data['project']
            role_project = RoleProject.objects.get(name="member")

            self.context["owner"] = ProjectConfirmInvitationCodeExecutorService.run(
                request_user=request_user,
                project=project,
                role_project=role_project
            )

            return project
        except Exception as e:
            raise DatabaseOperationException(
                f"User project or notification could not be created. {e}"
            )


class ProjectAddUserSerializer(serializers.Serializer):
    projects_selected = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Project.objects.all(),
        write_only=True,
        required=True,
        allow_empty=False,
        error_messages={
            'required': 'Projects selected is required.',
            'empty': 'You must select one project.'
        }
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=True,
        allow_null=False,
        error_messages={
            'required': 'User is required.',
            'null': 'User may not be blank.'
        }
    )

    def validate(self, data):
        request_user = self.context['request'].user
        max_users_per_project = request_user.plan_type.max_users

        data = ProjectAddUserValidator.run(
            data=data,
            request_user=request_user,
            max_users_per_project=max_users_per_project,
        )

        return data

    def create(self, validated_data):
        try:
            request_user = self.context['request'].user
            user = validated_data.get('user')
            project = validated_data.get('project')

            ProjectAddUserExecutorService.run(
                instance=project,
                request_user=request_user,
                user=user
            )

            return project
        except Exception:
            raise DatabaseOperationException(
                "User cannot add to the project."
            )
