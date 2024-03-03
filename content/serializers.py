from rest_framework import serializers
from .models import Post, Like, Mention, Viewer, Image, Video, Audio
from django.contrib.auth.models import User
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
    owner = UserSerializer(many=False)
    mentioned = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    total_viewed = serializers.SerializerMethodField(read_only=True)
    person_viewed = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    # total_post_view = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        
    def get_total_viewed(self, obj):
        return obj.total_view_count
    
    def get_mentioned(self, obj):
        mentioned_users = obj.mentioned_users
        return list(mentioned_users)

    def get_is_like(self, obj):
        request_user = self.context['request'].user
        return Like.objects.filter(user=request_user, post=obj).exists()

    def get_likes(self, obj):
        return obj.likes_count

    def get_person_viewed(self, obj):
        return obj.views_count
