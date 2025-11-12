from typing import Optional
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]:
        # توکن از کوکی گرفته میشه
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None  # یعنی هیچ توکنی نیست → DRF می‌ره سراغ بقیه کلاس‌ها (مثلاً AnonymousUser)

        # حالا decode و validate کنیم
        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)

        if not user:
            raise exceptions.AuthenticationFailed('User not found', code='user_not_found')

        return (user, validated_token)
