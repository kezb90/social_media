from django.urls import path
from .views import PostListView
app_name = 'content'
urlpatterns = [
    path('post_list/', PostListView.as_view(), name='post-list'),
]
