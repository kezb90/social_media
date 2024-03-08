from django.contrib import admin
from django.contrib.admin import register
from .models import Post, Like, Tag, ViewerPost, PostMedia

# Register your models here.


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1


class ViewerPostInline(admin.TabularInline):
    model = ViewerPost
    extra = 1


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class LikeInline(admin.TabularInline):
    model = Like
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
        "is_active",
        "get_view_count",
        "get_likes_count",
        "created_at",
        "updated_at",
    )
    list_editable = ["is_active"]
    list_display_links = ("id", "title")
    search_fields = ("title", "caption", "id")
    inlines = [LikeInline, TagInline, PostMediaInline]

    def get_view_count(self, obj):
        return obj.posts_viewed.count()

    get_view_count.short_description = "View Count"

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    get_likes_count.short_description = "like Count"


class ViewerPostAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "timestamp"]


class PostMediaAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "media", "order"]


admin.site.register(Post, PostAdmin)
admin.site.register(PostMedia, PostMediaAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ViewerPost, ViewerPostAdmin)
