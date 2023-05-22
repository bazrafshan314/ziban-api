from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class ZibanUserAdmin(UserAdmin):
    list_display = ("username", "email", "password")


admin.site.register(User, ZibanUserAdmin)
