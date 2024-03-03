from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from django.contrib.auth.models import User
from .models import Post
from accounts.models import Profile
from .serializers import UserSerializer, PostSerializer


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        profile = Profile.objects.get(user=user)
        followings = profile.get_followings()
        queryset = Post.objects.filter(is_story=False, is_active=True, user__in=followings)
        post_serializer = PostSerializer(queryset, many=True)
        return Response(post_serializer.data, status.HTTP_200_OK)
