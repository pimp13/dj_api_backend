from dataclasses import asdict
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.exceptions import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_app.dto.register import RegisterDto
from auth_app.serializers import RegisterSerializer, UserSerializer
from auth_app.service import AuthService


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            bodyData = RegisterDto(
                username=request.data["username"],
                email=request.data["email"],
                password=request.data["password"],
            )
            result = AuthService.register(bodyData)
            return JsonResponse(result)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
