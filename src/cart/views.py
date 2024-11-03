import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from accounts.forms import AddressForm
from accounts.models import Address
from cart.forms import OrderForm
# from cart.forms import OrderForm
from cart.models import Order


class AddressAndOrderView(LoginRequiredMixin, View):
    template_name = 'cart/shop-checkout.html'
    login_url = '/customers/login/'

    def get_cart_items_from_cookie(self, request):
        cart_items_cookie = request.COOKIES.get('cartItems', '[]')
        cart_items = json.loads(cart_items_cookie)
        return cart_items

    def calculate_order_total(self, cart_items):
        total = 0
        for item in cart_items:
            try:
                price = float(item.get('price_after_discount', 0))
                quantity = int(item.get('quantity', 0))
                total += price * quantity
            except (ValueError, TypeError):
                pass
        return round(total, 2)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.get_full_path()
            return HttpResponseRedirect(f"{self.login_url}?next={next_url}")

        customer = request.user.customer
        addresses = customer.address.all()
        cart_items = self.get_cart_items_from_cookie(request)
        order_total = self.calculate_order_total(cart_items)

        address_form = AddressForm()
        order_form = OrderForm()

        context = {
            'cart_items': cart_items,
            'order_total': order_total,
            'addresses': addresses,
            'address_form': address_form,
            'order_form': order_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        addresses = customer.address.all()

        address_form = AddressForm(request.POST)
        order_form = OrderForm(request.POST)

        if 'address_form' in request.POST and address_form.is_valid():
            address = address_form.save()
            customer.address.add(address)
            customer.save()
            return HttpResponseRedirect(request.path_info)

        elif 'order_form' in request.POST and order_form.is_valid():
            selected_address_id = request.POST.get('selected_address')
            if selected_address_id:
                selected_address = get_object_or_404(Address, id=selected_address_id)

            return HttpResponseRedirect(reverse_lazy('customers:profile'))

        cart_items = self.get_cart_items_from_cookie(request)
        order_total = self.calculate_order_total(cart_items)

        context = {
            'cart_items': cart_items,
            'order_total': order_total,
            'addresses': addresses,
            'address_form': address_form,
            'order_form': order_form,
        }
        return render(request, self.template_name, context)


class PurchaseView(TemplateView):
    template_name = 'cart/purchase_basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_items = []
        cart_cookie = self.request.COOKIES.get('cartItems')

        if cart_cookie:
            import json
            cart_items = json.loads(cart_cookie)

        context['cart_items'] = cart_items
        return context
