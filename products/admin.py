from adminsortable2.admin import SortableAdminMixin, SortableAdminBase, \
    SortableTabularInline, SortableInlineAdminMixin
from django.contrib import admin
import nested_admin
from feincms3.admin import TreeAdmin

from .models import (ProductColor, ProductImage, ProductVariant, Product, Size, Color, Category, Discount,
                     Review, Brand)


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant


class ProductImageSortableInline(SortableTabularInline):
    model = ProductImage
    readonly_fields = ['image_tag']


@admin.register(ProductColor)
class ProductColorAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ProductImageSortableInline]


class ProductImageSortableInlineNested(nested_admin.NestedTabularInline):
    model = ProductImage
    readonly_fields = ['image_tag']


class ProductColorInline(nested_admin.NestedTabularInline):
    model = ProductColor
    inlines = [ProductVariantInline, ProductImageSortableInlineNested]


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
