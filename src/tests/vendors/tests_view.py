from django.test import TestCase
from django.urls import reverse

from accounts.models import Address
from vendors.models import Staff, Shop
from django.contrib.auth.models import Permission


class StaffRegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('vendors:register')
        self.permission_is_owner = Permission.objects.get(codename='is_owner')
        self.permission_is_manager = Permission.objects.get(codename='is_manager')

    def test_staff_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors/page-account-register.html')
        self.assertIn('address_form', response.context)
        self.assertIn('shop_form', response.context)

    def test_staff_register_view_post_valid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '09123456789',
            'password1': 'password123',
            'password2': 'password123',
            'street': 'Main St',
            'city': 'Tehran',
            'state': 'Tehran',
            'zipcode': '1234567890',
            'name': 'Test Shop',
            'slug': 'test-shop',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.register_url)

        staff = Staff.objects.get(email='john.doe@example.com')
        self.assertEqual(staff.first_name, 'John')
        self.assertEqual(staff.type, 'owner')
        self.assertTrue(staff.check_password('password123'))
        self.assertTrue(staff.user_permissions.filter(codename='is_owner').exists())
        self.assertTrue(staff.user_permissions.filter(codename='is_manager').exists())

        shop = staff.shop
        self.assertEqual(shop.name, 'Test Shop')
        self.assertEqual(shop.address.street, 'Main St')

    def test_staff_register_view_post_invalid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '09123456789',
            'password1': 'password123',
            'password2': 'password456',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors/page-account-register.html')
        self.assertFalse(Staff.objects.filter(email='john.doe@example.com').exists())
        self.assertIn('Passwords must match.', response.context['form'].errors['password2'])



class CreateStaffViewTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(street='Main', city='Test City', state='Test',zipcode='01234565432')
        self.shop = Shop.objects.create(name="Test Shop",address=self.address)
        self.owner = Staff.objects.create_user(
            first_name="Owner",
            last_name="User",
            email="owner@example.com",
            phone="09123456789",
            password="password123",
            type="owner",
            shop=self.shop
        )
        self.owner.user_permissions.add(Permission.objects.get(codename='is_owner'))

        self.create_staff_url = reverse('vendors:create_staff')

    def test_create_staff_view_get(self):
        self.client.login(email="owner@example.com", password="password123")
        response = self.client.get(self.create_staff_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors/page-create-staff.html')
        self.assertIn('form', response.context)

    def test_create_staff_view_post_valid(self):
        self.client.login(email="owner@example.com", password="password123")
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '09123456780',
            'password1': 'password123',
            'password2': 'password123',
            'type': 'manager',
        }
        response = self.client.post(self.create_staff_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('vendors:register'))
        staff = Staff.objects.get(email='john.doe@example.com')
        self.assertEqual(staff.first_name, 'John')
        self.assertEqual(staff.shop, self.shop)
        self.assertEqual(staff.type, 'manager')
        self.assertTrue(staff.user_permissions.filter(codename='is_manager').exists())

    def test_create_staff_view_post_invalid(self):
        self.client.login(email="owner@example.com", password="password123")
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '09123456780',
            'password1': 'password123',
            'password2': 'password124',
            'type': 'manager',
        }
        response = self.client.post(self.create_staff_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors/page-create-staff.html')
        self.assertIn('Passwords must match.', response.context['form'].errors['password2'])
        self.assertFalse(Staff.objects.filter(email='john.doe@example.com').exists())

    def test_create_staff_view_permission_denied(self):
        non_owner = Staff.objects.create_user(
            first_name="Regular",
            last_name="User",
            email="user@example.com",
            phone="09123456781",
            password="password123",
            type="operator",
            shop=self.shop
        )
        self.client.login(email="user@example.com", password="password123")
        response = self.client.get(self.create_staff_url)

        self.assertEqual(response.status_code, 403)
