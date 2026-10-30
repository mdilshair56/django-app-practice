from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions import APIValidationError, ResourceNotFoundError
from auth.serializers.login_otp_serializer import (
    LoginOTPRequestSerializer,
    LoginOTPVerifySerializer,
)
from auth.services.user import LoginOTPService

User = get_user_model()


class LoginOTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginOTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # Find the active account before creating an OTP challenge.
        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user is None:
            raise ResourceNotFoundError(
                "Account with the provided email does not exist."
            )

        LoginOTPService.create_challenge(user)

        return Response(
            {
                "detail": (
                    "An OTP has been sent to your registered email address."
                )
            },
            status=status.HTTP_200_OK,
        )


class LoginOTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginOTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user is None:
            raise APIValidationError({
                "detail": "Invalid or expired login code."
            })

        valid, message = LoginOTPService.verify_challenge(
            user=user,
            submitted_otp=otp,
        )

        if not valid:
            raise APIValidationError({
                "detail": message,
            })

        # Issue JWT tokens only after successful OTP verification.
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "detail": "Login successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
