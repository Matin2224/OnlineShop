from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from dashboard.models import ShopProduct
from ...models import Order, ProductOrder

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['order', 'product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'delivered', 'order_address']
