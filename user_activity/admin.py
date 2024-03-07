from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "parent_comment",
        "content",
        "is_active",
        "created_at",
    )
    search_fields = ("user__username", "post__title", "content")
    list_editable = ["is_active"]


admin.site.register(Comment, CommentAdmin)
