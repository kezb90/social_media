from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostRetrieveUpdateDestroyView,
    PostViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("PostViewSet", PostViewSet, basename="viewsetpost")

app_name = "content"
urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:post_id>", PostDetailView.as_view(), name="post-detail"),
    path(
        "post_cbv/<pk>", PostRetrieveUpdateDestroyView.as_view(), name="post-list-cvb"
    ),
    path("viewsets/", include(router.urls)),
]
