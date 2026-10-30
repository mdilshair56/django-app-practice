from rest_framework import serializers
from auth.models.user import User
# from .user_profile_serializer import UserProfileSerializer
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(read_only=True)

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
        ]
        read_only_fields = fields

        # auth/api/me - Protected and Read Only!