from django.contrib import admin
from .models import CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
