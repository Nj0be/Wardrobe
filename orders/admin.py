from django.contrib import admin
from orders.models import Order, OrderItem, ReturnItem


class ReturnItemInline(admin.TabularInline):
     model = ReturnItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    inlines = [ReturnItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price', )
    inlines = [ReturnItem]


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return False
