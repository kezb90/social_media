from django.urls import path
from .views import PostListView, PostDetailView

app_name = "content"
urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:post_id>", PostDetailView.as_view(), name="post-detail"),
]
