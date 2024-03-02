from django.contrib import admin
from django.contrib.admin import register
from .models import Post, Image, Video, Audio

# Register your models here.


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
        "user",
        "title",
        "caption",
        "created_at",
        "updated_at",
        'is_active',
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "caption", "id")
    inlines = [ImageInline, VideoInline, AudioInline]
