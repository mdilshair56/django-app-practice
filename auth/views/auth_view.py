from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from common.exceptions import APIValidationError
from ..serializers import SignupSerializer
from ..serializers.reset_password_serializer import ResetPasswordSerializer
from ..serializers.token_serializer import CustomTokenObtainPairSerializer
from ..services.user import UserService


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(
            validated_data=serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "User registered successfully.",
                "data": SignupSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny], url_path="reset-password")
    def reset_password(self, request):
        data = (
            request.data.copy()
            if hasattr(request.data, "copy")
            else dict(request.data)
        )

        if "uid" not in data and "uid" in request.query_params:
            data["uid"] = request.query_params["uid"]
        if "token" not in data and "token" in request.query_params:
            data["token"] = request.query_params["token"]

        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        message = UserService.execute_password_reset(
            validated_data=serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": message,
                "data": None,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            raise APIValidationError({
                "refresh": "Refresh token is required to logout."
            })

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            raise APIValidationError({
                "refresh": "Invalid or expired refresh token."
            }) from exc

        return Response(
            {"success": True, "message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )

        