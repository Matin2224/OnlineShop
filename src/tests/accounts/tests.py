from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Address, User, Profile
import jdatetime


class AddressModelTest(TestCase):
    def test_create_address(self):
        address = Address.objects.create(
            street="street",
            city="city",
            state="state",
            zipcode="1234567890"
        )

        self.assertEqual(address.zipcode, "1234567890")
        self.assertEqual(address.city, "city")
        self.assertEqual(address.state, "state")
        self.assertEqual(address.street, "street")


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="tests@example.com",
            phone="09123456789",
            password="testpassword123",
            birthdate="2000-01-01"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "tests@example.com")
        self.assertEqual(self.user.phone, "09123456789")
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_persian_date_joined(self):
        persian_date = jdatetime.date.fromgregorian(date=self.user.date_joined).strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(self.user.persian_date_joined(), persian_date)

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.user.get_full_name())
