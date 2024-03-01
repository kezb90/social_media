from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from .serializers import SignupUserSerializer, LoginUserSerializer
from .permissions import IsUnauthenticated
from django.contrib.auth.models import User


# Create your views here.


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
                User.objects.create_user(username=username, password=password)
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
