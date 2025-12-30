from django.conf import settings

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from urllib.parse import urlparse


class HasValidOriginHeader(BasePermission):
    """
    Permission to allow access only from allowed origin headers.
    """

    def has_permission(self, request, view):
        """
        Checks if the request's Origin or Referer header is allowed.

        Args:
            request (HttpRequest): The current request object.
            view (View): The view being accessed.

        Raises:
            PermissionDenied: If origin header is missing or not allowed.

        Returns:
            bool: True if origin is allowed.
        """
        origin = request.headers.get('Origin') or request.headers.get('Referer')
        allowed_origins = settings.ALLOWED_HOSTS

        if not origin:
            raise PermissionDenied("Origin header missing.")

        parsed_origin = urlparse(origin)
        origin_host = parsed_origin.hostname

        if origin_host not in allowed_origins:
            raise PermissionDenied(f"Origin '{origin_host}' not allowed.")

        return True
