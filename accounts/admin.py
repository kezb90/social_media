from django.contrib import admin
from django.contrib.admin import register
from .models import Profile
# Register your models here.


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "age",
        "birthday",
        "created_at",
        'bio',
    )
    list_display_links = ("id", "user")
    search_fields = ("user__fisrt_name", "user__last_name", 'id')
