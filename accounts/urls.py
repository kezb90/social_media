from django.urls import path, include
from .views import SignUpView, LoginView, ProfileUpdateView, PublicProfileView
from .views import FollowerFollowingView, PublicProfileListView, FollowActionView, UnfollowActionView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:pk>/', PublicProfileView.as_view(), name='public-profile'),
    path('follower-following/', FollowerFollowingView.as_view(), name='follower-following'),
    path('public-profiles/', PublicProfileListView.as_view(), name='public-profiles'),
    path('follow/', FollowActionView.as_view(), name='follow-action'),
    path('unfollow/', UnfollowActionView.as_view(), name='unfollow-action'),

]
