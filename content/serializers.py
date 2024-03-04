from rest_framework import serializers
from .models import Post, Like, Mention, Viewer, Image, Video, Audio
# from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
        ]
        read_only_fields = ("username",)


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


class PostSerializer(serializers.ModelSerializer):
    mentioned = serializers.SerializerMethodField(read_only=True)
    # owner = UserSerializer(many=False )
    likes = serializers.SerializerMethodField(read_only=True)
    total_viewed = serializers.SerializerMethodField(read_only=True)
    person_viewed = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    # owner_username = UserSerializer(many=False )
    # total_post_view = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "caption",
            "mentioned",
            "likes",
            "total_viewed",
            "person_viewed",
            "is_like",
            "is_active",
            "is_story",
            "created_at",
            "updated_at",
        )
        # read_only_fields = ("owner",)

    def create(self, validated_data):
        request_user = self.context["request"].user

        # Check if the request user is the owner
        if request_user != validated_data["owner"]:
            raise PermissionDenied(
                "You do not have permission to create a post for another user."
            )

        return super().create(validated_data)

    def get_total_viewed(self, obj):
        return obj.total_view_count

    def get_mentioned(self, obj):
        mentioned_users = obj.mentioned_users
        return list(mentioned_users)

    def get_is_like(self, obj):
        request_user = self.context["request"].user
        return Like.objects.filter(user=request_user, post=obj).exists()

    def get_likes(self, obj):
        return obj.likes_count

    def get_person_viewed(self, obj):
        return obj.views_count
