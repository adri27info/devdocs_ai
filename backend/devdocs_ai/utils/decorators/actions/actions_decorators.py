def encapsule_refresh_decorator(decorator, exclude=None, **decorator_kwargs):
    """
    Apply a decorator to standard viewset actions, optionally excluding some actions.

    Args:
        decorator (function): The decorator to apply.
        exclude (set, optional): Actions to exclude from decoration.
        **decorator_kwargs: Keyword arguments to pass to the decorator.

    Returns:
        function: Class wrapper with decorators applied to viewset actions.
    """
    viewset_actions = {
        "list",
        "create",
        "retrieve",
        "update",
        "partial_update",
        "destroy",
        "change_password",
        "confirm_invitation_code",
        "add_user"
    }

    def wrapper(cls):
        """
        Wraps the class methods with the decorator.
        """
        for action_name in viewset_actions:
            if hasattr(cls, action_name):
                if exclude is None or action_name not in exclude:
                    original = getattr(cls, action_name)
                    decorated = decorator(**decorator_kwargs)(original)
                    setattr(cls, action_name, decorated)
        return cls

    return wrapper
