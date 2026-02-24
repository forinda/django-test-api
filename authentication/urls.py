from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
)

TaggedTokenRefreshView = extend_schema(tags=["Auth"])(TokenRefreshView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TaggedTokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
