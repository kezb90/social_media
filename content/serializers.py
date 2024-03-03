from rest_framework import serializers
from .models import Post, Like, Mention, Viewer, Image, Video, Audio
from django.contrib.auth.models import User


class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ("user", "post")


class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention
        fields = ("user", "post")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("user", "post")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]
        read_only_fields = ("username",)


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = "__all__"
