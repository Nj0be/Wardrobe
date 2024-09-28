from django.contrib import admin
from .models import *


class CartProductInline(admin.TabularInline):
    model = CartProduct


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [CartProductInline]