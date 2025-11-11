from rest_framework import status
from rest_framework.exceptions import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from auth_app.dto.register import RegisterDto
from auth_app.serializers import RegisterSerializer
from auth_app.service import AuthService
from utils.response import SuccessResponse


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(
                data=serializer.data, message="ثبت نام کاربر موفقیت آمیز بود"
            ).to_response()
        return ErrorResponse(
            data=serializer.errors, message="خطا در ثبت نام"
        ).to_response()


# Custom JWT login response
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # می‌توان اطلاعات اضافی اضافه کرد
        token["username"] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
