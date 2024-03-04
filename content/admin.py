from django.contrib import admin
from django.contrib.admin import register
from .models import Post, Image, Video, Audio, Like, Mention, Viewer

# Register your models here.


class ViewerInline(admin.TabularInline):
    model = Viewer
    extra = 1


class MentionInline(admin.TabularInline):
    model = Mention
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
    list_display = ("user", "post")


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "display_total_view_count",
        "display_likes",
        "display_views",
        "caption",
        "is_story",
        "created_at",
        "updated_at",
        "is_active",
    )

    def display_total_view_count(self, obj):
        return obj.total_view_count

    display_total_view_count.short_description = "total_views"

    def display_likes(self, obj):
        return obj.likes_count

    display_likes.short_description = "Likes"

    def display_views(self, obj):
        return obj.views_count

    display_views.short_description = "Person Views"

    list_display_links = ("id", "title")
    search_fields = ("title", "caption", "id")
    inlines = [
        ImageInline,
        VideoInline,
        AudioInline,
        LikeInline,
        MentionInline,
        ViewerInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
