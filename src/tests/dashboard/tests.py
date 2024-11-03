from django.test import TestCase
from django.urls import reverse
from accounts.models import Address
from customers.models import Customer
from website.models import Product, Category
from dashboard.models import Shop, ShopProduct, Rating, Comment
import jdatetime

class ShopModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Elm St", city="Tehran", state="Tehran", zipcode="1234567890"
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address,
        )
        self.address2 = Address.objects.create(
            street="123 Elm St", city="rasht", state="rasht", zipcode="1234567890"
        )

    def test_shop_creation(self):
        self.assertEqual(self.shop.name, "Test Shop")
        self.assertTrue(self.shop.active)
        self.assertEqual(self.shop.slug, "test-shop")
        self.assertIsInstance(self.shop, Shop)

    def test_shop_slug_generation(self):
        new_shop = Shop.objects.create(
            name="Test Shop",
            address=self.address2,
        )
        self.assertNotEqual(new_shop.slug, "test-shop")
        self.assertTrue(new_shop.slug.startswith("test-shop-"))

    def test_persian_create_at(self):
        persian_date = self.shop.persian_create_at()
        self.assertIsNotNone(persian_date)
        self.assertEqual(persian_date, jdatetime.date.fromgregorian(date=self.shop.created_at).strftime('%Y-%m-%d'))

class ShopProductModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Elm St", city="Tehran", state="Tehran", zipcode="1234567890"
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address,
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product",category=self.category)
        self.shop_product = ShopProduct.objects.create(
            shop=self.shop, product=self.product, price=100, discount=10, discount_type="PERCENTAGE", stock=50
        )

    def test_get_discounted_price(self):
        discounted_price = self.shop_product.get_discounted_price()
        self.assertEqual(discounted_price, 90.0)

class RatingModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Elm St", city="Tehran", state="Tehran", zipcode="1234567890"
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address,
        )
        self.customer = Customer.objects.create(email="customer@test.com", first_name="Test", last_name="Customer")
        self.rating = Rating.objects.create(user=self.customer, rating=5, content_object=self.shop)

    def test_rating_creation(self):
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.user.email, "customer@test.com")
        self.assertEqual(self.shop.rating_count, 1)
        self.assertEqual(self.shop.sum_rating, 5)
        self.assertEqual(self.shop.average_rating, 5.0)

class CommentModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Elm St", city="Tehran", state="Tehran", zipcode="1234567890"
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address,
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product",category=self.category)
        self.shop_product = ShopProduct.objects.create(
            shop=self.shop, product=self.product, price=100, discount=10, discount_type="PERCENTAGE", stock=50
        )
        self.customer = Customer.objects.create(email="customer@test.com", first_name="Test", last_name="Customer")
        self.comment = Comment.objects.create(user=self.customer, ShopProduct=self.shop_product, text="Great product!")

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, "Great product!")
        self.assertEqual(self.comment.status, "Submitted")
        self.assertEqual(self.comment.user.email, "customer@test.com")
        self.assertEqual(self.comment.ShopProduct.product.name, "Test Product")

    def test_update_status(self):
        self.comment.update_status("Approved")
        self.assertEqual(self.comment.status, "Approved")
