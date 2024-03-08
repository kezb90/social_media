from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from .models import Post, Like, Tag, ViewerPost, PostMedia
from accounts.models import Profile
from .serializers import (
    PostSerializer,
    LikeSerializer,
    TagSerializer,
    PostMediaSerializer,
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
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        get_object_or_404(Post, pk=post_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# region 1

# class PostViewSet(viewsets.ModelViewSet):
# queryset = Post.objects.all()
# serializer_class = PostSerializer
# permission_classes = [IsAuthenticated]


# def perform_create(self, serializer):
#     # Set the owner of the post to the authenticated user
#     serializer.save(owner=self.request.user.profile, is_active=True)

# def update(self, request, *args, **kwargs):
#     # Ensure users can only update their own posts
#     instance = self.get_object()
#     if instance.owner != self.request.user.profile:
#         return Response(
#             {"detail": "You do not have permission to perform this action."},
#             status=403,
#         )
#     return super().update(request, *args, **kwargs)

# def destroy(self, request, *args, **kwargs):
#     # Ensure users can only delete their own posts
#     instance = self.get_object()
#     if instance.owner != self.request.user.profile:
#         return Response(
#             {"detail": "You do not have permission to perform this action."},
#             status=403,
#         )
#     return super().destroy(request, *args, **kwargs)

# def get_object(self):
#     # Retrieve the post instance
#     post = super().get_object()

#     # Create a ViewerPost instance
#     user_profile = self.request.user.profile
#     if post.owner != self.request.user.profile:
#         ViewerPost.objects.create(user=user_profile, post=post)

#     return post
# end region
