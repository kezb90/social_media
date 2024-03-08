from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MediaFilter
from rest_framework import generics
from .models import Post, Like, Tag, ViewerPost, PostMedia
from accounts.models import Profile
from .serializers import (
    PostSerializer,
    LikeSerializer,
    TagSerializer,
    MediaSerializer,
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
    serializer_class = PostSerializer

    def get_queryset(self):
        # Only return posts for profile.is_public=True and user and user.followings
        owner_posts = Post.objects.filter(
            owner=self.request.user.profile, is_active=True
        )
        public_posts = Post.objects.filter(owner__is_public=True, is_active=True)
        followings_by_owner_profile = self.request.user.profile.followings
        represent_posts = Post.objects.none()
        for following in followings_by_owner_profile:
            represent_posts = represent_posts | Post.objects.filter(
                owner=following, is_active=True
            )

        return represent_posts | public_posts | owner_posts

    def get_object(self):
        if self.action not in ["retrieve"]:
            # Default behavior for list and retrieve actions
            post_id = self.kwargs.get("pk")
            obj: Post = get_object_or_404(
                Post.objects.filter(owner=self.request.user.profile), pk=post_id
            )
            return obj
        elif self.action in ["retrieve"]:
            post_id = self.kwargs.get("pk")
            obj = get_object_or_404(self.get_queryset(), pk=post_id)
            ViewerPost.objects.create(user=self.request.user.profile, post=obj)
            return super().get_object()
        else:
            return super().get_object()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class PostMediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = MediaFilter

    def get_queryset(self):
        return PostMedia.objects.filter(post__owner=self.request.user.profile)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.validated_data.get("post")
        if post.owner != self.request.user.profile:
            return Response(
                {
                    "detail": "You Can not manipulate the media of post you are not the owner."
                },
                status.HTTP_403_FORBIDDEN,
            )
        target_order = serializer.validated_data.get("order")
        is_in_order = post.post_media.filter(order=target_order).exists()
        if is_in_order:
            return Response(
                {
                    "detail": f"The order number {target_order} is in the orders of Media for the Post {post.id} ."
                },
                status.HTTP_403_FORBIDDEN,
            )
        serializer.save(post=post)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
