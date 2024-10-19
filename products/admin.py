from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
import nested_admin
from feincms3.admin import TreeAdmin

from .models import (ProductColor, ProductImage, ProductVariant, Product, Size, Color, Category, Discount,
                     Review, Brand)


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant


class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage


class ProductColorInline(nested_admin.NestedTabularInline):
    model = ProductColor
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductColorInline]

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    pass

@admin.register(Size)
class SizeAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(Color)
admin.site.register(Discount)
admin.site.register(Review)
admin.site.register(Brand)
