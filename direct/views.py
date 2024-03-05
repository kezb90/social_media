from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from django.db import models
from django.shortcuts import get_object_or_404
from accounts.models import Profile
import time
from django.http import HttpResponseBadRequest
from rest_framework.response import Response


class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(Profile, username=receiver_username)
        serializer.save(sender=self.request.user.profile, receiver=receiver)


class ReceivedMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by("-timestamp")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Implement long polling by holding the request for a maximum of 30 seconds
        for _ in range(5):
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

            time.sleep(1)  # Adjust the sleep time as needed

        return HttpResponseBadRequest("No new messages within the timeout.")


class AllUserMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        ).order_by("-timestamp")
