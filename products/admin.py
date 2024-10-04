from django.contrib import admin
import nested_admin
from .models import (ProductColor, ProductImage, ProductVariant, Product, Size, Color, Category, Discount,
                     Review, CartItem, Brand)


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant


class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage


class ProductColorInline(nested_admin.NestedTabularInline):
    model = ProductColor
    inlines = [ProductVariantInline, ProductImageInline]


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductColorInline]

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Review)
admin.site.register(Brand)
