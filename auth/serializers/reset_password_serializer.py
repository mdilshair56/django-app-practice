from rest_framework import serializers

from ..services.user import UserService


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    uid = serializers.CharField(required=False)
    token = serializers.CharField(required=False)
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
        required=False,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        required=False,
    )

    # Validates email (Step 1) or uid/token/passwords (Step 2) via UserService
    def validate(self, attrs):
        return UserService.validate_password_reset_data(attrs=attrs)