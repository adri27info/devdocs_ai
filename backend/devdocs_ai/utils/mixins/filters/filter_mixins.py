from django_filters.rest_framework import DjangoFilterBackend


class DjangoBaseFilterMixin:
    """
    Enables DjangoFilterBackend for viewsets.

    This mixin activates DjangoFilterBackend on any viewset that inherits from it. Each view
    must define its own `filterset_class` to specify filtering behavior.

    Attributes:
        filter_backends (list): List of active filter backends for the viewset.
    """
    filter_backends = [DjangoFilterBackend]
