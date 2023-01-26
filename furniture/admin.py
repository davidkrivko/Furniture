from django.contrib import admin

from furniture.models import (
    Furniture,
    Type,
    Commentary,
    Order,
    OrderItem,
)


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ["model", "type", "price"]
    list_filter = ["type"]
    search_fields = ["model"]


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 2


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin,)
    list_display = ["user", "created_time"]
    list_filter = ["user"]


admin.site.register(Order, OrderAdmin)
admin.site.register(Type)
admin.site.register(Commentary)
