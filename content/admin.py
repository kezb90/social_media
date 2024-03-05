from django.contrib import admin
from django.contrib.admin import register
from .models import Post, Image, Video, Audio, Like, Tag, Viewer

# Register your models here.


class ViewerInline(admin.TabularInline):
    model = Viewer
    extra = 1


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class LikeInline(admin.TabularInline):
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


class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post")


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "title",
        "caption",
        "created_at",
        "updated_at",
        "is_active",
    )

    list_display_links = ("id", "title")
    search_fields = ("title", "caption", "id")
    inlines = [
        ImageInline,
        VideoInline,
        AudioInline,
        LikeInline,
        TagInline,
        ViewerInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Viewer)
