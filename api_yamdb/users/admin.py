from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name", "bio", "role"
    )
    empty_value_display = "значение отсутствует"
    list_editable = ("role", "bio")
    list_filter = ("username",)
    search_fields = ("username", "role")


admin.site.register(User, UserAdmin)
