from rest_framework import serializers
from .models import Profile, Follow


class UnfollowActionSerializer(serializers.Serializer):
    target_username = serializers.CharField(max_length=30)
class FollowActionSerializer(serializers.Serializer):
    target_username = serializers.CharField(max_length=30)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "bio",
            "email",
            "password",
            "is_public",
            "profile_picture",
        )


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
        read_only_fields =['username']


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
