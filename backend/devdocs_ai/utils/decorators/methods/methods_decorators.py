from functools import wraps

from utils.services.exception.exception_response_service import (
    ExceptionResponseHandlerService
)
from utils.services.user.tokens.refresh_token.refresh_token_revocator_service import (
    RefreshTokenRevocatorService
)


def validate_refresh_token(require_active=True, revoke=True):
    """
    Decorator to validate and optionally revoke a refresh token before a view call.

    Args:
        require_active (bool, optional): Require the user to be active. Defaults to True.
        revoke (bool, optional): Revoke the token after validation. Defaults to True.

    Returns:
        function: Wrapped view method with refresh token validation applied.
    """
    def decorator(view_method):
        @wraps(view_method)
        def _wrapped(self, request, *args, **kwargs):
            """
            Wrapper that validates and revokes the refresh token.

            Attaches the validated user to `request.refresh_token_user`.
            """
            try:
                user = RefreshTokenRevocatorService(
                    require_active=require_active,
                    revoke=revoke
                ).run(request=request)

                request.refresh_token_user = user

                return view_method(self, request, *args, **kwargs)
            except Exception as e:
                return ExceptionResponseHandlerService.run(exc=e)

        return _wrapped
    return decorator
