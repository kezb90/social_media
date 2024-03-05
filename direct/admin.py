from django.contrib import admin
from .models import Message, Video, Audio, Image


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class AudioInline(admin.StackedInline):
    model = Audio
    extra = 1


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("timestamp", "sender", "receiver")

    inlines = [VideoInline, ImageInline, AudioInline]
