from django.contrib import admin
from django.contrib.admin import register
from .models import Post, Image, Video, Audio, Like, Mention, Viewer

# Register your models here.

class ViewerInline(admin.StackedInline):
    model = Viewer
    extra = 1

class MentionInline(admin.StackedInline):
    model = Mention
    extra = 1

class LikeInline(admin.StackedInline):
    model = Like
    extra = 1
        
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class AudioInline(admin.StackedInline):
    model = Audio
    extra = 1


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "caption",
        "is_story",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "caption", "id")
    inlines = [ImageInline, VideoInline, AudioInline, LikeInline, MentionInline,ViewerInline]
