from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


# Authentication Serializer


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "email",
            "password",
            "confirm_password",
        ]

    def save(self):
        username = self.validated_data["username"]
        full_name = self.validated_data["full_name"]
        email = self.validated_data["email"]

        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Password doesn't match"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User(
            email=email,
            full_name=full_name,
            username=username,
        )
        user.set_password(password)
        user.is_active = False
        user.save()

        return user


class OTPCodeSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "access_token", "refresh_token"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credential.")
        if not user.is_active:
            raise AuthenticationFailed("Email is not active")
        tokens = user.tokens()
        return {
            "email": user.email,
            "full_name": user.full_name,
            "access_token": str(tokens.get("access")),
            "refresh_token": str(tokens.get("refresh")),
        }




class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")

        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail("bad_token")






