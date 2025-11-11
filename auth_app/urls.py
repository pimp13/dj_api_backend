from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth_app.views import MyTokenObtainPairView, RegisterView, UserInfoView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("info", UserInfoView.as_view())
]
