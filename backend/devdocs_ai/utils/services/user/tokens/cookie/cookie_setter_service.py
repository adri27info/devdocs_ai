from utils.exceptions.instance.instance_exceptions import (
    InstanceInvalidValueException
)
from utils.general_utils import GeneralUtils


class CookieSetterService:
    """
    Service to set cookies on a Django HttpResponse with configurable options.
    """

    __MAX_AGE = 24 * 60 * 60
    __HTTP_ONLY = True
    __SECURE = False
    __SAMESITE = "Lax"
    __PATH = "/"

    def __init__(
        self,
        *,
        max_age=None,
        httponly=None,
        secure=None,
        samesite=None,
        path=None
    ):
        """
        Initializes the cookie setter with optional configuration parameters.

        Args:
            max_age (int, optional): Cookie expiration in seconds. Defaults 86400.
            httponly (bool, optional): Whether cookie is HTTP-only. Defaults True.
            secure (bool, optional): Whether cookie is secure. Defaults False.
            samesite (str, optional): SameSite attribute. Defaults "Lax".
            path (str, optional): Path scope of the cookie. Defaults "/".
        """
        self.max_age = GeneralUtils.use_default_if_none(
            value=max_age,
            default=self.__MAX_AGE
        )
        self.httponly = GeneralUtils.use_default_if_none(
            value=httponly,
            default=self.__HTTP_ONLY
        )
        self.secure = GeneralUtils.use_default_if_none(
            value=secure,
            default=self.__SECURE
        )
        self.samesite = GeneralUtils.use_default_if_none(
            value=samesite,
            default=self.__SAMESITE
        )
        self.path = GeneralUtils.use_default_if_none(
            value=path,
            default=self.__PATH
        )

    def run(
        self,
        *,
        response,
        key,
        value,
    ):
        """
        Sets a cookie on the given Django response with configured options.

        Args:
            response (HttpResponse): The Django response object.
            key (str): The cookie key.
            value (str): The cookie value.

        Raises:
            InstanceInvalidValueException: If response, key, or value is invalid.
        """
        if not response:
            raise InstanceInvalidValueException("Invalid or missing response param.")

        if not key:
            raise InstanceInvalidValueException("Cookie key must be a non-empty string.")

        if not value:
            raise InstanceInvalidValueException("Cookie value must be a non-empty string.")

        response.set_cookie(
            key=key,
            value=value,
            max_age=self.max_age,
            httponly=self.httponly,
            secure=self.secure,
            samesite=self.samesite,
            path=self.path,
        )
