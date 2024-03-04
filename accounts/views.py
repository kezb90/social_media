from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    FollowerFollowingSerializer,
    PublicProfileSerializer,
)
from .permissions import IsUnauthenticated
from .models import Profile


# Create your views here.
class SignUpView(generics.CreateAPIView):
    permission_classes = [IsUnauthenticated]
    queryset = Profile.objects.all()
    serializer_class = SignUpSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is valid, generate JWT tokens
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            # Invalid credentials
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PublicProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.filter(is_public=True)
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.AllowAny]


class FollowerFollowingView(generics.RetrieveAPIView):
    serializer_class = FollowerFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class PublicProfileListView(generics.ListAPIView):
    serializer_class = PublicProfileSerializer
    queryset = Profile.objects.filter(is_public=True)
    permission_classes = [permissions.IsAuthenticated]
