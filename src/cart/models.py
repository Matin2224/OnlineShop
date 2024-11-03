import jdatetime
from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Address
from customers.models import Customer
from dashboard.models import ShopProduct


# Customer = apps.get_model('cart', 'Customer')
# ShopProduct = apps.get_model('cart', 'ShopProduct')


class Order(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders",
                                 verbose_name=_("Customer"))
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                  verbose_name=_("Total Payment"))
    ORDER_STATUS_CHOICES = [
        ("Preparing", _("Preparing")),
        ("Sending", _("Sending")),
        ("Completed", _("Completed"))
    ]
    delivered = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=100, verbose_name=_("Order Status"))
    shop_product = models.ManyToManyField(ShopProduct, through="ProductOrder", related_name="orders_shop_product")
    order_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name=_("Order Address"))

    def update_delivered(self, new_delivered):
        if new_delivered in dict(self.ORDER_STATUS_CHOICES):
            self.delivered = new_delivered
            self.save()

    def calculate_payment(self):
        total_payment = 0
        for product_order in self.productorder_set.all():
            total_payment += product_order.total_price
        self.payment = total_payment
        return self.payment

    def persian_create_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.create_at).strftime('%Y-%m-%d')
        return persian_date

    def __str__(self):
        return f'{self.customer} has a total payment of {self.payment:.2f} created on {self.persian_create_at()}'


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, verbose_name=_("Product"),related_name="productorder")
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Total Price"))

    def __str__(self):
        return f'Product: {self.product.product.name}, Quantity: {self.quantity}, Total Price: {self.total_price}'

    @classmethod
    def calculate(cls, order, product, quantity):
        order_item = cls(order=order, product=product, quantity=quantity)
        order_item.calc_total_price()
        order_item.save()

    def calc_total_price(self):
        self.total_price = self.quantity * self.product.price
