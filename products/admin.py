from django.contrib import admin
from .models import ProductColorImage, ProductVariant, Product, Size, Color, Category, Discount, Review, CartItem


class ProductColorImageInline(admin.TabularInline):
    model = ProductColorImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorImageInline, ProductVariantInline]

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Review)
