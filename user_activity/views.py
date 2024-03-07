from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from content.models import Post
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get posts by request.user
        user_posts = Post.objects.filter(owner=self.request.user.profile)

        # Get the profiles followings by request.user
        followings = self.request.user.profile.followings

        following_profiles_posts = Post.objects.none()
        for profile in followings:
            following_profiles_posts = following_profiles_posts | profile.posts.filter(
                is_active=True
            )
        all_posts = user_posts | following_profiles_posts

        all_comments = Comment.objects.none()
        for post in all_posts:
            all_comments = all_comments | Comment.objects.filter(
                post=post, is_active=True
            )
        return all_comments

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user.profile)

    def update(self, request, *args, **kwargs):

        instance: Comment = self.get_object()

        instance.is_active = True
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
