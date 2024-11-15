from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegistrationView,
    VerifyUserView,
    LoginView,
    LogoutView,

)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/", VerifyUserView.as_view(), name="verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
  
]
