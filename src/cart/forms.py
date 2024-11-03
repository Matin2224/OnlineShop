from django import forms

from cart.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_address']
