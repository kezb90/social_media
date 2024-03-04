from django.urls import path, include
from .views import SignUpView, LoginView, ProfileUpdateView, PublicProfileView
from .views import FollowerFollowingView, PublicProfileListView

app_name = "accounts"

urlpatterns = [
    # path("profile/update/", profileUpdateView, name="profile-update"),
    # path("profile/follow_list/<str:username>", followListView, name="follow-list"),
    # path("profile/follow/<str:username>", follow, name="follow"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:pk>/', PublicProfileView.as_view(), name='public-profile'),
    path('follower-following/', FollowerFollowingView.as_view(), name='follower-following'),
    path('public-profiles/', PublicProfileListView.as_view(), name='public-profiles'),
]
