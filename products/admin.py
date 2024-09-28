from django.contrib import admin
from .models import *


class ProductColorImageInline(admin.TabularInline):
    model = ProductColorImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


# class DiscountInline(admin.TabularInline):
    # model = Discount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorImageInline, ProductVariantInline]

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)