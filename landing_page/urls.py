from django.urls import path
from .views import landing_page, about_us

app_name = "home"
urlpatterns = [
    path("", landing_page, name="main"),
    path("about_us", about_us, name="about-us"),
]
