# messaging/api/urls.py
from django.urls import path
from .views import SendMessageAPIView, ReceivedMessagesAPIView, AllUserMessagesAPIView

app_name = 'direct'
urlpatterns = [
    path('send_message/<str:receiver_username>/', SendMessageAPIView.as_view(), name='send_message_api'),
    path('received_messages/', ReceivedMessagesAPIView.as_view(), name='received_messages_api'),
    path('all_user_messages/', AllUserMessagesAPIView.as_view(), name='all_user_messages_api'),
]
