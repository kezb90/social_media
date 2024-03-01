from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from django.db import IntegrityError
from .serializers import (
    SignupUserSerializer,
    LoginUserSerializer,
    ProfileSerializer,
    UserSerializer,
)
from .permissions import IsUnauthenticated
from django.contrib.auth.models import User
from .models import Profile
from rest_framework import generics
from django.shortcuts import get_object_or_404


# Create your views here.


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profileUpdateView(request: Request):
    if request.method == "GET":
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"error": "This profile does not exist."}, status.HTTP_404_NOT_FOUND
            )

    if request.method == "PUT":
        user_data = UserSerializer(data=request.data.get("user")).initial_data
        user_id = user_data.get("id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."}, status.HTTP_404_NOT_FOUND
            )

        if request.user == user:
            user_Serializer = UserSerializer(data=request.data.get("user"))
            if user_Serializer.is_valid():
                user.first_name = user_Serializer.data.get("first_name")
                user.last_name = user_Serializer.data.get("last_name")
                user.email = user_Serializer.data.get("email")
                user.save()
            else:
                return Response(user_Serializer.errors, status.HTTP_400_BAD_REQUEST)

            profile_serializer = ProfileSerializer(data=request.data)
            if profile_serializer.is_valid():
                profile_id = request.data.get("id")
                try:
                    user_profile = Profile.objects.get(pk=profile_id)
                except Profile.DoesNotExist:
                    return Response(
                        {"message": "You can not access other user profile"}
                    )
                profile = Profile.objects.get(user=request.user)
                if user_profile == profile:
                    profile.birthday = profile_serializer.data.get("birthday")
                    profile.bio = profile_serializer.data.get("bio")
                    profile.is_active = profile_serializer.data.get("is_active")
                    profile.is_public = profile_serializer.data.get("is_public")
                    profile.save()
                else:
                    return Response(
                        profile_serializer.errors, status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(profile_serializer.errors, status.HTTP_400_BAD_REQUEST)

            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"message": "You cant Update other Profiles!"},
                status.HTTP_403_FORBIDDEN,
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful."}, status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@permission_classes([IsUnauthenticated])
def registerUser(request: Request):
    if request.method == "POST":
        serializer = SignupUserSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.data.get("username")
            password = serializer.data.get("password")
            try:
                # Create the user
                user = User.objects.create_user(username=username, password=password)
                # Create the profile for the user
                Profile.objects.create(user=user, is_active=True)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except IntegrityError:
                # Handle the case where the username already exists
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsUnauthenticated])
def loginUser(request: Request):
    if request.method == "POST":
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                return Response(
                    {"message": "Login successful."}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid username or password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
