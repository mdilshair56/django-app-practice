
from rest_framework import serializers

from auth.models.user_profile import UserProfile
from auth.serializers.user_serializer import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "father_name",
            "date_of_birth",
            "address",
            "city",
            "state",
            "country",
        ]
