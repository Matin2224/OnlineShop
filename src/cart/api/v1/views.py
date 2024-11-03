from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from accounts.models import Address
from ...models import Order, ProductOrder, ShopProduct
from .serializers import OrderSerializer, ProductOrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Order, ProductOrder, ShopProduct
from .serializers import OrderSerializer, ProductOrderSerializer


class CreateOrderView(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request, *args, **kwargs):
        customer = request.user.customer

        selected_address_id = request.data.get('selected_address')
        selected_address = get_object_or_404(Address, id=selected_address_id) if selected_address_id else None

        order_data = {
            "customer": customer.id,
            "delivered": "Preparing",
            "order_address": selected_address.id if selected_address else None
        }

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            errors = []
            for item in request.data.get('shop_products', []):
                try:

                    shop_product = ShopProduct.objects.get(id=item['id'])

                except ShopProduct.DoesNotExist:
                    errors.append(f"Product with ID {item['id']} does not exist.")
                    continue

                total_price = round(shop_product.get_discounted_price() * item['quantity'], 2)
                shop_product.stock -= item['quantity']
                shop_product.save()
                product_order_data = {
                    "order": order.id,
                    "product": shop_product.id,
                    "quantity": item['quantity'],
                    "total_price": total_price
                }

                product_order_serializer = ProductOrderSerializer(data=product_order_data)

                if not product_order_serializer.is_valid():
                    errors.append(product_order_serializer.errors)
                    continue

                try:
                    product_order_serializer.save()

                except Exception as e:
                    print("Exception while saving ProductOrderSerializer:", str(e))
                    errors.append(str(e))

            order.calculate_payment()
            order.save()

            response = Response({"success": True}, status=status.HTTP_201_CREATED)
            response.delete_cookie('cartItems')
            return response
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
