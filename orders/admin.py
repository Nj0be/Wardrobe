from django.contrib import admin
from orders.models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('price', )


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

    def has_delete_permission(self, request, obj=None):
        return False
