from rest_framework import serializers
from .models import Post, Like, Tag, ViewerPost
from rest_framework.exceptions import PermissionDenied
from accounts.serializers import ProfileSerializer


class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewerPost
        fields = ("user", "post")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "user", "post")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "caption",
        ]


class PostSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(read_only=True)
    likes = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "caption",
            "likes",
        ]

    def create(self, validated_data):
        request_user = self.context["request"].user

        # Check if the request user is the owner
        if request_user != validated_data["owner"]:
            raise PermissionDenied(
                "You do not have permission to create a post for another user."
            )

        return super().create(validated_data)
