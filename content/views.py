from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from .models import Post, Like, Tag
from .serializers import (
    PostSerializer,
    PostCreateUpdateSerializer,
    LikeSerializer,
    TagSerializer,
)
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class AddTagView(generics.CreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()


class RemoveTagView(generics.DestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()


class AddLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()


class RemoveLikeView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return posts for the authenticated user
        return Post.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        # Set the owner of the post to the authenticated user
        serializer.save(owner=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        # Ensure users can only update their own posts
        instance = self.get_object()
        if instance.owner != self.request.user.profile:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Ensure users can only delete their own posts
        instance = self.get_object()
        if instance.owner != self.request.user.profile:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        return super().destroy(request, *args, **kwargs)
