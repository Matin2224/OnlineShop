from django.test import TestCase
from customers.models import Customer
from accounts.models import Address
from cart.models import ShopProduct, Order, ProductOrder
from dashboard.models import Shop
from website.models import Category, Product


class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(email="test@example.com")
        self.address = Address.objects.create(street="123 Main St", city="Test City", state="test", zipcode="12345")
        self.address2 = Address.objects.create(street="124 Main St", city="Test City", state="test", zipcode="12345")
        self.shop = Shop.objects.create(name="Test Shop", address=self.address2)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category)
        self.shop_product = ShopProduct.objects.create(shop=self.shop, product=self.product, price=500)
        self.order = Order.objects.create(
            customer=self.customer,
            delivered="Preparing",
            order_address=self.address
        )
        self.product_order = ProductOrder.objects.create(
            order=self.order,
            product=self.shop_product,
            quantity=2
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.delivered, "Preparing")
        self.assertEqual(self.order.order_address, self.address)
        self.assertEqual(self.order.payment, 0)

    def test_order_str(self):
        expected_str = f'{self.customer} has a total payment of 0.00 created on {self.order.persian_create_at()}'
        self.assertEqual(str(self.order), expected_str)

    def test_order_update_delivered(self):
        self.order.update_delivered("Completed")
        self.assertEqual(self.order.delivered, "Completed")

    def test_order_calculate_payment(self):
        self.product_order.calc_total_price()
        self.product_order.save()
        # self.order.calculate_payment()
        self.assertEqual(self.order.calculate_payment(), 1000)

    def test_persian_create_at(self):
        persian_date = self.order.persian_create_at()
        self.assertIsNotNone(persian_date)
        self.assertEqual(len(persian_date.split('-')), 3)

class ProductOrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(email="test@example.com")
        self.address = Address.objects.create(street="123 Main St", city="Test City", state="test", zipcode="12345")
        self.address2 = Address.objects.create(street="124 Main St", city="Test City", state="test", zipcode="12345")
        self.shop = Shop.objects.create(name="Test Shop", address=self.address2)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category)
        self.shop_product = ShopProduct.objects.create(shop=self.shop, product=self.product, price=500)
        self.order = Order.objects.create(
            customer=self.customer,
            delivered="Preparing",
            order_address=self.address
        )

    def test_product_order_creation(self):
        product_order = ProductOrder.objects.create(order=self.order, product=self.shop_product, quantity=3)
        self.assertEqual(product_order.order, self.order)
        self.assertEqual(product_order.product, self.shop_product)
        self.assertEqual(product_order.quantity, 3)
        self.assertEqual(product_order.total_price, 0)

    def test_product_order_str(self):
        product_order = ProductOrder.objects.create(order=self.order, product=self.shop_product, quantity=3)
        expected_str = f'Product: {self.shop_product.product.name}, Quantity: {product_order.quantity}, Total Price: {product_order.total_price}'
        self.assertEqual(str(product_order), expected_str)

    def test_product_order_calc_total_price(self):
        product_order = ProductOrder.objects.create(order=self.order, product=self.shop_product, quantity=3)
        product_order.calc_total_price()
        self.assertEqual(product_order.total_price, 1500)

    def test_product_order_calculate_classmethod(self):
        ProductOrder.calculate(order=self.order, product=self.shop_product, quantity=4)
        self.assertEqual(ProductOrder.objects.count(), 1)
        created_order = ProductOrder.objects.first()
        self.assertEqual(created_order.total_price, 2000)
