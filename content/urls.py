from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet

from .views import AddTagView
from .views import RemoveTagView
from .views import RemoveLikeView
from .views import AddLikeView
from .views import PostMediaViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"postmedia", PostMediaViewSet, basename="postmedia")

app_name = "content"

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/add-like/", AddLikeView.as_view(), name="add-like"),
    path("api/remove-like/<int:pk>/", RemoveLikeView.as_view(), name="remove-like"),
    path("api/add-tag/", AddTagView.as_view(), name="add-tag"),
    path("api/remove-tag/<int:pk>/", RemoveTagView.as_view(), name="remove-tag"),
]
