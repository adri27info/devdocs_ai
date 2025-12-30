import django_filters

from apps.notifications.models import Notification


class NotificationFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(
        field_name="type",
        lookup_expr="iexact"
    )

    class Meta:
        model = Notification
        fields = ["type"]
