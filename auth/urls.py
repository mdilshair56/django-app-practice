from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from auth.views.login_otp_view import (
    LoginOTPRequestView,
    LoginOTPVerifyView,
)

from .views.auth_view import AuthViewSet
from .views.profile_view import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")
router.register(r"users", UserViewSet, basename="users")
router.register(r"profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("login/request-otp/", LoginOTPRequestView.as_view(), name="login-request-otp",),
    path("login/verify-otp/", LoginOTPVerifyView.as_view(), name="login-verify-otp",),
]