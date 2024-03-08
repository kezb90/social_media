from rest_framework import serializers
from .models import Post, Like, Tag, ViewerPost, PostMedia
from rest_framework.exceptions import PermissionDenied
from accounts.serializers import ProfileSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["id", "post", "media", "order"]


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["id", "media", "order"]


class PostSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "caption",
            "like_count",
            "view_count",
            "post_media",
        ]
        read_only_fields = ["likes", "view_count"]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_view_count(self, obj):
        return obj.posts_viewed.count()


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
