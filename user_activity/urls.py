from django.urls import path
from .views import CommentListCreateView, CommentDetailView

app_name = "user_activity"
urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
