from django.contrib import admin
from .models import *


class CartProductInline(admin.TabularInline):
    model = CartProduct


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CartProductInline]