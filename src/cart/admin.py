from django.contrib import admin

from django.contrib import admin
from .models import Order, ProductOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'payment', 'delivered', 'create_at')
    search_fields = ('customer', 'delivered')
    list_filter = ('delivered',)


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'total_price')
    search_fields = ('product', 'order')
    list_filter = ('order',)


