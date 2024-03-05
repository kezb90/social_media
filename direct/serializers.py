from rest_framework import serializers
from .models import Message, Image
from accounts.models import Profile


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "caption"]


class MessageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username"]


class MessageSerializer(serializers.ModelSerializer):
    sender = MessageProfileSerializer(read_only=True, many=False)
    receiver = MessageProfileSerializer(read_only=True, many=False)
    image = ImageSerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "image", "timestamp"]
