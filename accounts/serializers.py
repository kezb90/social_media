from rest_framework import serializers
from .models import Profile, Follow, FollowRequest
from django.core.exceptions import ValidationError
import re


class UnfollowActionSerializer(serializers.Serializer):
    target_username = serializers.CharField(max_length=30)


class FollowActionSerializer(serializers.Serializer):
    target_username = serializers.CharField(max_length=30)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "bio",
            "email",
            "is_public",
            "profile_picture",
        ]


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "bio",
            "password",
            "is_public",
            "profile_picture",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def validate_username(self, value):
        """
        Custom validator for the 'username' field.
        """
        if not value.startswith("@"):
            raise ValidationError("Username must start with '@'.")

        if len(value) <= 4:
            raise ValidationError("Username must be more than 4 characters long.")

        if not re.match(r"^[@\w.+-]+$", value):
            raise ValidationError(
                "Invalid characters in the username. Only letters, digits, '@', '.', '+', '-', and '_' are accepted."
            )

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "is_public",
            "bio",
            "profile_picture",
        )
        read_only_fields = ["username"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]


class FollowerFollowingSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "username", "follower", "following"]

    def get_follower(self, obj):
        followers = Follow.objects.filter(following=obj)
        return FollowSerializer(followers, many=True).data

    def get_following(self, obj):
        following = Follow.objects.filter(follower=obj)
        return FollowSerializer(following, many=True).data


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "is_public", "bio", "profile_picture"]


class FollowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowRequest
        fields = ["id", "from_user", "to_user", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["from_user"] = Profile.objects.get(
            pk=instance.from_user.id
        ).username
        representation["to_user"] = Profile.objects.get(pk=instance.to_user.id).username
        return representation
