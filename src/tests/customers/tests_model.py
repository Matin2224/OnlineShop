from django.test import TestCase
from django.db.utils import IntegrityError
from customers.models import Customer, CustomerProfile, Address


class CustomerModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="1234567890"
        )

        self.customer = Customer.objects.create_user(
            email="customer@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.customer.address.add(self.address)

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertFalse(self.customer.is_staff)
        self.assertFalse(self.customer.is_superuser)
        self.assertTrue(self.customer.is_customer)
        self.assertIn(self.address, self.customer.address.all())

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Customer: John Doe")

    def test_customer_profile_created(self):
        profile = CustomerProfile.objects.get(user=self.customer)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.customer)

    def test_customer_profile_updated(self):
        self.customer.first_name = "Jane"
        self.customer.save()
        self.customer.refresh_from_db()
        profile = CustomerProfile.objects.get(user=self.customer)
        self.assertEqual(self.customer.first_name, "Jane")
        self.assertEqual(profile.user.first_name, "Jane")


class CustomerProfileModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create_user(
            email="customer2@example.com",
            password="password123",
            first_name="Alice",
            last_name="Smith"
        )

    def test_customer_profile_str(self):
        profile = CustomerProfile.objects.get(user=self.customer)
        self.assertEqual(str(profile), f"Profile of {self.customer.email}")

    def test_customer_profile_creation(self):
        profile = CustomerProfile.objects.get(user=self.customer)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.customer)
