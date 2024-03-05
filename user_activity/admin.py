from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "parent_comment", "content", "created_at")
    search_fields = ("user__username", "post__title", "content")


admin.site.register(Comment, CommentAdmin)
