from rest_framework import serializers

from auth.models.user import User
from .user_profile_serializer import UserProfileSerializer
from ..services.user import UserService


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_superuser",
            "password",
            "profile",
        ]
        read_only_fields = ["id", "is_superuser",]

    def validate_password(self, value):
        return UserService.validate_user_password(password=value)