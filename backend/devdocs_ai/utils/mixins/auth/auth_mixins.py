from utils.services.user.tokens.cookie.auth.cookie_auth_checker_service import (
    CookieAuthCheckerService
)


class NoAuthMixin:
    """
    Mixin to disable authentication on a view.
    """
    authentication_classes = []


class CookieJWTAuthMixin:
    """
    Mixin to enable cookie-based JWT authentication on a view.
    """
    authentication_classes = [CookieAuthCheckerService]
