from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from django.db import models
from django.shortcuts import get_object_or_404
from accounts.models import Profile


class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(Profile, username=receiver_username)
        serializer.save(sender=self.request.user.profile, receiver=receiver)


class UserMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_username = self.kwargs.get("sender_username")
        sender = get_object_or_404(Profile, username=sender_username)
        query = Message.objects.filter(
            sender=sender, receiver=self.request.user.profile
        ) | Message.objects.filter(sender=self.request.user.profile, receiver=sender)
        return query.order_by("-timestamp")


class AllUserMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        ).order_by("-timestamp")
