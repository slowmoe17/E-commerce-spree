from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import Login, Register , ValidateOtp

app_name = "users"


urlpatterns = [
    path("login/", Login.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("register/", Register.as_view()),
    path("validate_otp/", ValidateOtp.as_view()),
]
