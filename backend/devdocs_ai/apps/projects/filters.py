import django_filters

from apps.projects.models import Project


class ProjectFilter(django_filters.FilterSet):
    privacy = django_filters.CharFilter(
        field_name="privacy",
        lookup_expr="iexact"
    )
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Project
        fields = ["privacy", "name"]
