from django.contrib import admin
from .models import CartItem, User


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]