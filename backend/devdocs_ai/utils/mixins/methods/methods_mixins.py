class ExcludeHTTPMethodsMixin:
    """
    Mixin to exclude specified HTTP methods from a DRF ModelViewSet.

    Usage:
        class UserViewSet(ExcludeHTTPMethodsMixin, ModelViewSet):
            exclude_methods = ['post', 'delete']
            # 'post' disables the create action
            # 'delete' disables the destroy action
    """

    exclude_methods = []

    def __init_subclass__(cls, **kwargs):
        """
        Filter out HTTP methods from http_method_names at class creation.
        """
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "http_method_names"):
            cls.http_method_names = [
                m for m in cls.http_method_names
                if m not in getattr(cls, "exclude_methods", [])
            ]
