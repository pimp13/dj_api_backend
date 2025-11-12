from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGIRequest):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return

        token = request.COOKIES.get('access_token')
        if not token:
            request.user = None
            return

        jwt_auth = JWTAuthentication()

        try:
            validation_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validation_token)
            request.user = user
        except (InvalidToken, AuthenticationFailed):
            request.user = None
            return
