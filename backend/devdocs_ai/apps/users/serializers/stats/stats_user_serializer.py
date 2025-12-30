from django.db.models import Count

from rest_framework import serializers

from apps.users_projects.models import UserProject
from apps.plans_types.serializers import PlanTypeSerializer


class StatsUserSerializer(serializers.Serializer):
    plan_type = PlanTypeSerializer(read_only=True)
    owned_projects = serializers.SerializerMethodField()
    involved_projects = serializers.SerializerMethodField()

    def get_owned_projects(self, instance):
        owner_projects = UserProject.objects.filter(
            user=instance,
            role_project__name="owner"
        ).select_related(
            'project'
        ).annotate(
            current_users=Count('project__users')
        )

        return [
            {
                "id": up.project.id,
                "name": up.project.name,
                "privacy": up.project.privacy,
                "current_users": up.current_users,
                "max_users": instance.plan_type.max_users,
            }
            for up in owner_projects
        ]

    def get_involved_projects(self, instance):
        user_projects = UserProject.objects.filter(
            user=instance
        ).select_related(
            'project', 'role_project', 'user'
        ).annotate(
            current_users=Count('project__users')
        )

        projects_data = []

        for up in user_projects:
            owner_up = UserProject.objects.filter(
                project=up.project,
                role_project__name="owner"
            ).select_related(
                'user'
            ).first()

            if owner_up:
                max_users = owner_up.user.plan_type.max_users
            else:
                max_users = up.user.plan_type.max_users

            projects_data.append({
                "id": up.project.id,
                "name": up.project.name,
                "privacy": up.project.privacy,
                "current_users": up.current_users,
                "max_users": max_users,
            })

        unique_projects = {p["id"]: p for p in projects_data}.values()
        return list(unique_projects)
