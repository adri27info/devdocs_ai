from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieAuthCheckerService(JWTAuthentication):
    """
    JWT authentication service using access token from cookies.
    """

    def authenticate(self, request):
        """
        Authenticates a user based on the access token stored in cookies.

        Args:
            request (HttpRequest): Django request object.

        Raises:
            InvalidToken: If the access token is missing, invalid, or expired.

        Returns:
            tuple: User instance and validated token if authentication succeeds,
            None if access token cookie is missing.
        """
        access_token = request.COOKIES.get('accesstoken')
        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except Exception:
            raise InvalidToken("Access token is invalid or has expired.")
