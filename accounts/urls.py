from django.urls import path, include
from .views import SignUpView
from .views import LoginView
from .views import ProfileUpdateView
from .views import ProfileRetrieveAPIView
from .views import FollowerFollowingRetrieveAPIView
from .views import ProfileListView
from .views import FollowerFollowingListAPIView
from .views import FollowActionView
from .views import UnfollowActionView
from .views import send_follow_request
from .views import FollowRequestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("requests", FollowRequestViewSet, basename="follow-request")

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "follower-following/<int:pk>",
        FollowerFollowingRetrieveAPIView.as_view(),
        name="follower-following-detail",
    ),
    path(
        "follower-following/",
        FollowerFollowingListAPIView.as_view(),
        name="follower-following-list",
    ),
    path("profile/", ProfileListView.as_view(), name="profile-list"),
    path("profile/<int:pk>/", ProfileRetrieveAPIView.as_view(), name="profile-detail"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("follow/", FollowActionView.as_view(), name="follow-action"),
    path("unfollow/", UnfollowActionView.as_view(), name="unfollow-action"),
    path(
        "api/send_follow_request/<str:target_username>/",
        send_follow_request,
        name="send_follow_request",
    ),
    path("follow_request/", include(router.urls)),
]
