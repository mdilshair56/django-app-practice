from rest_framework import serializers


class LoginOTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # password = serializers.CharField(
    #     write_only=True,
    #     trim_whitespace=False,
    # )


class LoginOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.RegexField(
        regex=r"^\d{6}$",
        error_messages={
            "invalid": "OTP must contain exactly six digits."
        },
    )