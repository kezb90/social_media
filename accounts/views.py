from django.contrib.auth import authenticate
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    FollowerFollowingSerializer,
    PublicProfileSerializer,
    FollowActionSerializer,
    UnfollowActionSerializer,
    FollowRequestSerializer,
)
from rest_framework.decorators import api_view, permission_classes, action
from .permissions import IsUnauthenticated
from .models import Profile, Follow, FollowRequest, ViewProfile


class UnfollowActionView(generics.DestroyAPIView):
    serializer_class = UnfollowActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        target_username = self.request.data.get("target_username", "")
        try:
            target_profile = Profile.objects.get(username=target_username)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({"error": "This profile does not exist"})
        return target_profile

    def destroy(self, request, *args, **kwargs):
        target_profile = self.get_object()
        follower_profile = request.user.profile

        # Check if the follow relationship exists
        follow_instance = Follow.objects.filter(
            follower=follower_profile, following=target_profile
        ).first()
        if follow_instance:
            follow_instance.delete()
            return Response(
                {"message": f"You have unfollowed {target_profile.username}"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowActionView(generics.CreateAPIView):
    serializer_class = FollowActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_username = serializer.validated_data["target_username"]
        try:
            target_profile = Profile.objects.get(username=target_username)
        except Profile.DoesNotExist:
            return Response(
                {"error": "This profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if Follow.objects.filter(
            follower=request.user.profile, following=target_profile
        ).exists():
            return Response(
                {"message": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target_profile.is_public:
            follower_profile = request.user.profile

            # Check if the follow relationship already exists
            if not Follow.objects.filter(
                follower=follower_profile, following=target_profile
            ).exists():
                follow_instance = Follow.objects.create(
                    follower=follower_profile, following=target_profile
                )
                return Response(
                    {"message": f"You are now following {target_profile.username}"},
                    status=status.HTTP_201_CREATED,
                )

        else:
            return Response(
                {"error": "This is a private profile. You should send follow request."},
                status=status.HTTP_403_FORBIDDEN,
            )


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


class FollowerFollowingListAPIView(generics.ListAPIView):
    serializer_class = FollowerFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get public profiles
        public_profiles = Profile.objects.filter(is_public=True, is_active=True)

        # Get profiles followed by the authenticated user
        following_profiles = Profile.objects.filter(
            followers__follower=self.request.user.profile, is_active=True
        )

        # Combine both sets of profiles
        profiles = public_profiles | following_profiles

        return profiles


class FollowerFollowingRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = FollowerFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get public profiles
        public_profiles = Profile.objects.filter(is_public=True, is_active=True)

        # Get profiles followed by the authenticated user
        following_profiles = Profile.objects.filter(
            followers__follower=self.request.user.profile, is_active=True
        )

        # Combine both sets of profiles
        profiles = public_profiles | following_profiles

        return profiles


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get public profiles
        public_profiles = Profile.objects.filter(is_public=True, is_active=True)

        # Get profiles followed by the authenticated user
        following_profiles = Profile.objects.filter(
            followers__follower=self.request.user.profile, is_active=True
        )

        # Combine both sets of profiles
        profiles = public_profiles | following_profiles

        return profiles

    def get_object(self):
        # Retrieve the profile instance
        profile = super().get_object()

        # Create a ViewProfile instance
        viewed_profile = profile
        viewer_profile = self.request.user.profile
        if viewed_profile != viewer_profile:
            view_profile_instance = ViewProfile.objects.create(
                viewer=viewer_profile, viewed_profile=viewed_profile
            )

        return profile


class ProfileListView(generics.ListAPIView):
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get public profiles
        public_profiles = Profile.objects.filter(is_public=True, is_active=True)

        # Get profiles followed by the authenticated user
        following_profiles = Profile.objects.filter(
            followers__follower=self.request.user.profile, is_active=True
        )

        # Combine both sets of profiles
        profiles = public_profiles | following_profiles

        return profiles


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_follow_request(request, target_username):

    try:
        target_profile = Profile.objects.get(username=target_username)
    except Profile.DoesNotExist:
        return Response(
            {"error": f"Profile with username {target_username} not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_profile = request.user.profile

    # Check if the user is already following the target profile
    if target_profile in request.user.profile.followings:
        return Response(
            {"message": f"You are already following {target_profile.username}."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if the target profile is public
    if target_profile.is_public:
        Follow.objects.create(follower=user_profile, following=target_profile)
        return Response(
            {"message": f"Follow request sent to {target_profile.username}."},
            status=status.HTTP_201_CREATED,
        )
    else:
        # Check if a follow request already exists
        if FollowRequest.objects.filter(
            from_user=user_profile, to_user=target_profile
        ).exists():
            return Response(
                {
                    "message": f"Follow request to {target_profile.username} is already pending."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new follow request
        follow_request_data = {
            "from_user": user_profile.pk,
            "to_user": target_profile.pk,
        }
        follow_request_serializer = FollowRequestSerializer(data=follow_request_data)
        if follow_request_serializer.is_valid():
            follow_request_serializer.save()
            return Response(
                {"message": f"Follow request sent to {target_profile.username}."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Invalid follow request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        follow_requests = FollowRequest.objects.filter(
            to_user=self.request.user
        ) | FollowRequest.objects.filter(from_user=self.request.user)
        return follow_requests

    def update(self, request, *args, **kwargs):
        # Custom logic or raise an exception to indicate that updates are not allowed
        return Response(
            {"detail": "Updates are not allowed."}, status=status.HTTP_403_FORBIDDEN
        )

    def create(self, request, *args, **kwargs):
        # Ensure from_user is set to request.user.profile
        if request.data["from_user"] != str(request.user.profile.pk):
            return Response(
                {"detail": "You cannot follow a user on behalf of another user."},
                status.HTTP_403_FORBIDDEN,
            )

        if request.data["to_user"] == str(request.user.profile.pk):
            return Response(
                {"detail": "You cannot follow yourself."}, status.HTTP_403_FORBIDDEN
            )

        # Use the serializer to create the FollowRequest object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = serializer.validated_data.get("to_user")
        from_user: Profile = serializer.validated_data.get("from_user")
        if to_user in from_user.followings:
            return Response(
                {"detail": "You are already following this user."},
                status.HTTP_403_FORBIDDEN,
            )
        else:
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    @action(detail=True, methods=["POST"])
    def accept_follow_request(self, request, pk=None):
        follow_request = self.get_object()
        # Check if the request user is the receiver of the follow request
        if follow_request.to_user != request.user.profile:
            return Response(
                {"detail": "You can only accept follow requests addressed to you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        Follow.objects.create(
            follower=follow_request.from_user,
            following=follow_request.to_user,
        )

        # Delete the FollowRequest instance
        follow_request.delete()

        return Response(
            {"detail": "Follow request accepted successfully."},
            status=status.HTTP_200_OK,
        )
