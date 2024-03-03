from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from django.contrib.auth.models import User
from .models import Post, Like, Viewer, Mention
from accounts.models import Profile
from .serializers import UserSerializer, PostSerializer
from django.db.utils import IntegrityError
from django.db.models import F


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, post_id: int):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "This Post does not exist."}, status.HTTP_404_NOT_FOUND
            )
        profile = Profile.objects.get(user=post.user)
        post_serializer = PostSerializer(post, many=False)
        if request.user in profile.get_followers() or request.user == profile.user:
            viewer = Viewer(user=request.user, post=post, is_active=True, count=1)
            try:
                viewer.save()
            except IntegrityError:
                viewer, created = Viewer.objects.update_or_create(
                    user_id=request.user.id,
                    post_id=post_id,
                    defaults={"count": F("count") + 1},
                )
            return Response(post_serializer.data, status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": f"You should follow the user {post.user} to see his/her posts."
                },
                status.HTTP_403_FORBIDDEN,
            )


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        profile = Profile.objects.get(user=user)
        followings = profile.get_followings()
        queryset = Post.objects.filter(
            is_story=False, is_active=True, user__in=followings
        )
        post_serializer = PostSerializer(queryset, many=True)
        return Response(post_serializer.data, status.HTTP_200_OK)
