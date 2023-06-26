from django.contrib import admin
from .models import User, Product, Category, CartItem
from django.contrib.auth.admin import UserAdmin


class ZibanUserAdmin(UserAdmin):
    list_display = ("username", "email", "password")


admin.site.register(User, ZibanUserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
