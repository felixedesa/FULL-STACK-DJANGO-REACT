# user/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and displaying user information.
    """
    class Meta:
        model = User
        fields = [
            'id', 'public_id', 'username', 'first_name',
            'last_name', 'email', 'is_active', 'created', 'updated'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration requests and creating new users.
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'password', 'confirm_password'
        ]

    def validate(self, data):
        """
        Validate that the password and confirm_password fields match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")

        # Optional: Validate password strength
        validate_password(data['password'])

        return data

    def create(self, validated_data):
        """
        Create and return a new user using the custom create_user method.
        """
        validated_data.pop('confirm_password')  # Remove confirm_password field
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for handling user login with JWT token generation.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
