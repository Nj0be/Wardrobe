from django.contrib import admin
from orders.models import Order, OrderItem


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price', )


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

    def has_delete_permission(self, request, obj=None):
        return False
