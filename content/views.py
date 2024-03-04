from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Post, Like, Viewer, Mention
from accounts.models import Profile, Follow
from .serializers import UserSerializer, PostSerializer
from django.db.utils import IntegrityError
from django.db.models import F
from .permissions import IsOwnerOnly, IsOwnerorAccessReadOnly_Post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerorAccessReadOnly_Post]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        users_followed_by_user = Follow.objects.filter(follower = self.request.user.profile)
        print(users_followed_by_user)
        # Users that current user is allowed to see their post
        # users_allowed = users_followed_by_user | Profile.objects.filter(
        #     username=self.request.user
        # )

        return Post.objects.filter(owner= self.request.user)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerorAccessReadOnly_Post]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, post_id: int):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "This Post does not exist."}, status.HTTP_404_NOT_FOUND
            )
        profile = Profile.objects.get(username=post.owner)
        post_serializer = PostSerializer(post, context={"request": request}, many=False)
        if request.user in profile.get_followers() or request.user == profile.username:
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
                    "message": f"You should follow the user {post.owner} to see his/her posts."
                },
                status.HTTP_403_FORBIDDEN,
            )


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        profile = Profile.objects.get(username=request.user)
        followings = Follow.objects.filter(follower = profile)
        queryset = Post.objects.filter(
            is_story=False, is_active=True)
        post_serializer = PostSerializer(
            queryset, context={"request": request}, many=True
        )
        return Response(post_serializer.data, status.HTTP_200_OK)
