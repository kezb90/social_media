from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
import re


class SignupUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50)
    password_2 = serializers.CharField(max_length=50)

    class Meta:
        fields = [
            "username",
            "password",
            "password_2",
        ]

    def validate_password(self, password):
        if password != self.initial_data.get("password_2"):
            raise serializers.ValidationError("Password does not match!.")
        return password

    def validate_username(self, username):

        pattern = re.compile(r"^@.*$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                'Invalid username. It must start with "@" and contain only lowercase letters, numbers, and underscores.'
            )

        pattern = re.compile(r"^.{5,20}$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                "Invalid username length. The username must be between 5 and 20 characters."
            )

        pattern = re.compile(r"^@[a-zA-Z_][a-zA-Z0-9_]*$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                'Invalid username format. It must start with "@" followed by a letter or underscore, and can contain only letters, numbers, and underscores.'
            )

        return username
        """
        {
        "username":"@mohsen",
        "password":"sss",
        "password_2":"sss"
        }
        """


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50)

    def validate_username(self, username):

        pattern = re.compile(r"^@.*$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                'Invalid username. It must start with "@" and contain only lowercase letters, numbers, and underscores.'
            )

        pattern = re.compile(r"^.{5,20}$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                "Invalid username length. The username must be between 5 and 20 characters."
            )

        pattern = re.compile(r"^@[a-zA-Z_][a-zA-Z0-9_]*$")
        if not bool(pattern.match(username)):
            raise serializers.ValidationError(
                'Invalid username format. It must start with "@" followed by a letter or underscore, and can contain only letters, numbers, and underscores.'
            )

        return username

    """
        {
        "username":"@mohsen",
        "password":"sss"
        }
    """
