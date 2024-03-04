from django.contrib import admin
from django.contrib.admin import register
from .models import Profile, Follow

# Register your models here.


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_public",
        "bio",
    )
    list_display_links = ("id", "username")
    search_fields = ("fisrt_name", "last_name", "id")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]
    search_fields = ["follower__username", "following__username"]
    list_filter = ["created_at", "follower", "following"]
