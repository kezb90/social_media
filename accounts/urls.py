from django.urls import path, include
from .views import registerUser, loginUser, logout_view
from .views import profileUpdateView, followListView, follow

app_name = "accounts"

urlpatterns = [
    path("register/", registerUser, name="signup"),
    path("login/", loginUser, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/update/", profileUpdateView, name="profile-update"),
    path("profile/follow_list/<str:username>", followListView, name="follow-list"),
    path("profile/follow/<str:username>", follow, name="follow"),
]
