from adminsortable2.admin import SortableAdminMixin, SortableAdminBase, \
    SortableTabularInline, SortableInlineAdminMixin
from django.contrib import admin
import nested_admin
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms.widgets import SelectMultiple
from feincms3.admin import TreeAdmin

from .models import (ProductColor, ProductImage, ProductVariant, Product, Size, Color, Category, Discount,
                     Review, Brand)


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant
    ordering = ('size',)


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


# Custom Field Class for category to display full name (with ancestors)
class CustomCategoryChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        parent_category = obj.parent
        parent_str = ''
        while parent_category:
            parent_str = f'{parent_category.name} - ' + parent_str
            parent_category = parent_category.parent
        return parent_str + f'{obj.name}'


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductColorInline]

    # We set the custom field class for categories
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs['form_class'] = CustomCategoryChoiceField
            kwargs['queryset'] = Category.objects.order_by('position')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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
