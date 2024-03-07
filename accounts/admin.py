from django.contrib import admin
from django.contrib.admin import register
from .models import Profile, Follow, FollowRequest, ViewProfile

# Register your models here.


# Inline class for followers
class FollowersInline(admin.TabularInline):
    model = Follow
    fk_name = "following"
    verbose_name_plural = "Followers"
    extra = 1


# Inline class for following users
class FollowingInline(admin.TabularInline):
    model = Follow
    fk_name = "follower"
    verbose_name_plural = "Following"
    extra = 1


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_active",
        "get_followers_list",  # Add the custom method to list_display
        "get_following_list",  # Add the custom method to list_display
        "is_public",
        "bio",
    )
    list_editable = ["is_active"]
    list_display_links = ("id", "username")
    search_fields = ("fisrt_name", "last_name", "id")
    inlines = [FollowersInline, FollowingInline]

    # Custom method to get the list of followers as a string
    # Custom method to get the list of followers as a string
    def get_followers_list(self, obj):
        followers = obj.followers.all()
        return ", ".join([follower.follower.username for follower in followers])

    get_followers_list.short_description = "Followers"  # Set the column header

    # Custom method to get the list of following users as a string
    def get_following_list(self, obj):
        following = obj.following.all()
        return ", ".join([followed.following.username for followed in following])

    get_following_list.short_description = "Following"  # Set the column header


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]
    search_fields = ["follower__username", "following__username"]
    list_filter = ["created_at", "follower", "following"]


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    list_filter = ("from_user", "to_user", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        # Disable the ability to add FollowRequest instances through the admin interface
        return False


class ViewProfileAdmin(admin.ModelAdmin):
    list_display = ("viewer", "viewed_profile", "timestamp")
    list_filter = ("timestamp", "viewer", "viewed_profile")
    search_fields = ("viewer__username", "viewed_profile__username")
    date_hierarchy = "timestamp"


admin.site.register(ViewProfile, ViewProfileAdmin)
