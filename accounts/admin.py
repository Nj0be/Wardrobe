from django.contrib import admin
from .models import User
from products.admin import CartItemInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
