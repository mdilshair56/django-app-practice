from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth.models.user_profile import UserProfile
from ..serializers import UserSerializer
from ..serializers.user_profile_serializer import UserProfileSerializer
from ..services.user import IsAdminOrReadOnlyClient, UserService

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles:
      - GET /api/auth/users/
      - GET /api/auth/users/<id>/
      - GET /api/auth/users/me/
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnlyClient]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """GET /api/auth/users/me/"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles:
      - GET /api/auth/profiles/
      - GET /api/auth/profiles/<id>/
      - GET /api/auth/profiles/mine/
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrReadOnlyClient]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="mine",
    )
    def my_profile(self, request):
        """GET /api/auth/profiles/mine/"""
        profile = UserService.get_or_create_user_profile(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)