from django.urls import path
from .views import SendMessageAPIView, AllUserMessagesAPIView, UserMessagesAPIView

app_name = "direct"
urlpatterns = [
    path(
        "send_message/<str:receiver_username>/",
        SendMessageAPIView.as_view(),
        name="send_message_api",
    ),
    path(
        "all_user_messages/",
        AllUserMessagesAPIView.as_view(),
        name="all_user_messages_api",
    ),
    path(
        "user_messages/<str:sender_username>/",
        UserMessagesAPIView.as_view(),
        name="user_messages_api",
    ),
]
