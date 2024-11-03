from django.test import TestCase
from accounts.models import User, Address
from dashboard.models import Shop
from vendors.models import Staff, StaffProfile
from django.contrib.auth.models import Permission

class StaffModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="1234567890"
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address
        )

        self.staff = Staff.objects.create_user(
            email="staff@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            type="owner",
            shop=self.shop
        )

    def test_staff_creation(self):
        self.assertEqual(self.staff.first_name, "John")
        self.assertEqual(self.staff.last_name, "Doe")
        self.assertTrue(self.staff.is_staff)
        self.assertFalse(self.staff.is_superuser)
        self.assertTrue(self.staff.is_active)
        self.assertEqual(self.staff.type, "owner")
        self.assertEqual(self.staff.shop, self.shop)

    def test_staff_str(self):
        self.assertEqual(str(self.staff), "John Doe")

    def test_staff_profile_created(self):
        profile = StaffProfile.objects.get(user=self.staff)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.staff)

    def test_staff_profile_updated(self):
        self.staff.first_name = "Jane"
        self.staff.save()
        profile = StaffProfile.objects.get(user=self.staff)
        self.assertEqual(self.staff.first_name, "Jane")
        self.assertEqual(profile.user.first_name, "Jane")

    def test_staff_permissions(self):
        permissions = self.staff._meta.permissions
        self.assertIn(("is_owner", "Is owner"), permissions)
        self.assertIn(("is_manager", "Is manager"), permissions)


class StaffProfileModelTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="123 Main St",
            city="Test City",
            state="Test State",
            zipcode="1234567890"
        )

        self.shop = Shop.objects.create(
            name="Test Shop",
            address=self.address
        )

        self.staff = Staff.objects.create_user(
            email="staff2@example.com",
            password="password123",
            first_name="Alice",
            last_name="Smith",
            type="manager",
            shop=self.shop
        )

    def test_staff_profile_str(self):
        profile = StaffProfile.objects.get(user=self.staff)
        self.assertEqual(str(profile), f"Profile: {profile.bio}")

    def test_staff_profile_creation(self):
        profile = StaffProfile.objects.get(user=self.staff)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.staff)
