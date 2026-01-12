from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Follow

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
    "username",
    "name",
    "email", 
    "bio",
    "avatar",
    "banner",
    "verified",
    "created_at",
    "follower_count", 
    "following_count",
    "location", 
    "website",
    "birth_date",
    )
    list_filter = (
    "username",
    "email",
    "created_at",
    "location", 
    )

    fieldsets = (
    ("Account Info", {
        "fields": (
            "username",
            "email",
            "verified",
        )
    }),

    ("Personal Details", {
        "fields": (
            "name",
            "bio",
            "birth_date",
            "location",
            "website",
        )
    }),

    ("Profile Media", {
        "fields": (
            "avatar",
            "banner",
        )
    }),

    ("Social Stats", {
        "fields": (
            "follower_count",
            "following_count",
        )
    }),
    ("Dates", {"fields": ("last_login", "date_joined")}),
)
    add_fieldsets = (
        (None, {
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    search_fields = ("username", "email")

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    search_fields = ("follower__username", "following__username")
    list_filter = ("created_at",)