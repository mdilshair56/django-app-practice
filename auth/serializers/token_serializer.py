
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .user_serializer import UserSerializer
from ..services.user import UserService


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = UserSerializer(self.user).data

        return UserService.build_login_response(
            token_data=data,
            user_data=user_data,
        )