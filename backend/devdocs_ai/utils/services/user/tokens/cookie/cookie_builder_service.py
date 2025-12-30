from django.conf import settings
from django.middleware.csrf import get_token

from rest_framework_simplejwt.tokens import RefreshToken

from utils.services.user.tokens.cookie.cookie_setter_service import CookieSetterService
from utils.general_utils import GeneralUtils


class CookieBuilderService:
    """
    Service to generate authentication and CSRF cookies for a user session.
    """

    __INCLUDE_ACCESS = True
    __INCLUDE_REFRESH = True
    __INCLUDE_CSRF = True
    __REMEMBER_ME = False

    def __init__(
        self,
        *,
        include_access=None,
        include_refresh=None,
        include_csrf=None,
        remember_me=None,
    ):
        """
        Initializes the cookie builder with optional inclusion flags.

        Args:
            include_access (bool, optional): Whether to include access token cookie.
            include_refresh (bool, optional): Whether to include refresh token cookie.
            include_csrf (bool, optional): Whether to include CSRF cookie.
            remember_me (bool, optional): Whether to extend refresh token lifetime.
        """
        self.include_access = GeneralUtils.use_default_if_none(
            value=include_access,
            default=self.__INCLUDE_ACCESS
        )
        self.include_refresh = GeneralUtils.use_default_if_none(
            value=include_refresh,
            default=self.__INCLUDE_REFRESH
        )
        self.include_csrf = GeneralUtils.use_default_if_none(
            value=include_csrf,
            default=self.__INCLUDE_CSRF
        )
        self.remember_me = GeneralUtils.use_default_if_none(
            value=remember_me,
            default=self.__REMEMBER_ME
        )

    def run(self, *, response, request, user):
        """
        Generates authentication and CSRF cookies for a given user.

        Args:
            response (HttpResponse): Django response to attach cookies.
            request (HttpRequest): Django request object for CSRF token.
            user (User): The user instance to generate tokens for.

        Returns:
            tuple: A tuple containing the response and a dictionary describing
                the cookies set with their properties.
        """
        refresh = None

        if self.include_csrf:
            request.META.pop("CSRF_COOKIE", None)

        if self.include_access or self.include_refresh:
            refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token) if refresh else None
        refresh_token = str(refresh) if refresh else None
        refresh_lifetime = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

        cookies_to_set = {
            "accesstoken": {
                "include": self.include_access,
                "value": access_token,
                "max_age": int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                "httponly": True,
            },
            "refreshtoken": {
                "include": self.include_refresh,
                "value": refresh_token,
                "max_age": refresh_lifetime * 2 if self.remember_me else refresh_lifetime,
                "httponly": True,
            },
            "csrftoken": {
                "include": self.include_csrf,
                "value": get_token(request) if self.include_csrf else None,
                "max_age": int(settings.CSRF_COOKIE_AGE.total_seconds()),
                "httponly": False,
            },
        }

        for key, props in cookies_to_set.items():
            if props["include"] and props["value"] is not None:
                cookie_instance = CookieSetterService(
                    max_age=props["max_age"],
                    httponly=props["httponly"],
                )

                cookie_instance.run(
                    response=response,
                    key=key,
                    value=props["value"],
                )

        return response, cookies_to_set
