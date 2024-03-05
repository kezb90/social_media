from django.urls import path
from .views import SignUpView
from .views import LoginView
from .views import ProfileUpdateView
from .views import ProfileRetrieveAPIView
from .views import FollowerFollowingRetrieveAPIView
from .views import ProfileListView
from .views import FollowerFollowingListAPIView
from .views import FollowActionView
from .views import UnfollowActionView

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
]
