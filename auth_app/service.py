from django.contrib.auth.models import User
from auth_app.dto.login import LoginDto
from auth_app.dto.register import RegisterDto
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def login(bodyData: LoginDto):
        pass

    @staticmethod
    def register(bodyData: RegisterDto):
        if User.objects.filter(username=bodyData.username).first():
            raise ValueError("Username already exists")

        user = User(username=bodyData.username, email=bodyData.email)
        user.set_password(bodyData.password)
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            "username": user.username,
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
