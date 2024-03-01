from django.urls import path, include
from .views import registerUser, loginUser, logout_view

app_name = "accounts"

urlpatterns = [
    path("register/", registerUser, name="signup"),
    path("login/", loginUser, name="login"),
    path("logout/", logout_view, name="logout"),
]
