from django.shortcuts import redirect
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from accounts.models import User
from customers.forms import CustomerRegisterModelForm
from customers.models import Customer


class CustomerRegisterViewTests(TestCase):

    def setUp(self):
        self.url = reverse('customers:register')
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'rajabi',
            'phone': '09123456789',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        self.invalid_data = {
            'first_name': '',
            'last_name': '',
            'phone': '123456789',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123',
        }

    def test_register_view_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        self.assertTrue(Customer.objects.filter(email='testuser@example.com').exists())

        user = Customer.objects.get(email='testuser@example.com')
        self.assertTrue(user.check_password('strongpassword123'))

        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_register_view_form_invalid(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertFalse(Customer.objects.filter(email='invalid-email').exists())

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/page-login-register.html')
        self.assertIsInstance(response.context['form'], CustomerRegisterModelForm)


class CustomerLoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create_user(
            email='testuser@example.com',
            phone='09123456789',
            password='testpassword123',
            is_customer=True
        )
        self.login_url = reverse_lazy('customers:login')  # Update with your actual URL name
        self.verify_url = reverse_lazy('customers:verify')  # Update with your actual URL name

    def test_login_with_email(self):
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'testpassword123',
        })
        self.assertRedirects(response, reverse('customers:profile'))

    def test_login_with_phone_sends_sms_code(self):
        response = self.client.post(self.login_url, {
            'login': '09123456789',
            'password': 'testpassword123',
        })
        self.assertRedirects(response, self.verify_url)
        self.assertIn('code', self.client.session)
        self.assertIn('authenticated_user_id', self.client.session)

    def test_login_invalid_form(self):
        response = self.client.post(self.login_url, {
            'login': '',
            'password': '',
        })
        self.assertFormError(response, 'form', 'login', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

class CodeVerificationViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create_user(
            email='testuser@example.com',
            phone='09123456789',
            password='testpassword123',
            is_customer=True
        )
        self.client.session['authenticated_user_id'] = self.customer.id
        self.client.session['code'] = 123456
        self.verify_url = reverse_lazy('customers:verify')  # Update with your actual URL name

    def test_code_verification_success(self):
        response = self.client.post(self.verify_url, {
            'code': '123456',
        })
        # self.assertEqual(response.status_code,302)
        # self.assertRedirects(response, reverse_lazy('customers:profile'))
        self.assertNotIn('code', self.client.session)
        self.assertNotIn('authenticated_user_id', self.client.session)

    def test_code_verification_invalid_form(self):
        response = self.client.post(self.verify_url, {
            'code': '',
        })
        self.assertFormError(response, 'form', 'code', 'This field is required.')



#
# class CodeVerificationViewTests(TestCase):
#
#     def setUp(self):
#         self.customer = Customer.objects.create_user(email="customer@example.com", phone="09123456789", password="testpassword")
#         self.client = Client()
#         self.verification_url = reverse('customers:verify')
#         self.client.cookies['code'] = '123456'
#         self.client.cookies['user_id'] = str(self.customer.id)
#
#
#
#     def test_invalid_code_verification(self):
#         data = {'code': '654321'}
#         response = self.client.post(self.verification_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'code', 'Invalid verification code')
#
#     def test_code_verification_with_no_code_cookie(self):
#         self.client.cookies['code'] = ''
#         data = {'code': '123456'}
#         response = self.client.post(self.verification_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'code', 'Invalid verification code')
#
#
# class CustomerLoginViewTests(TestCase):
#
#     def setUp(self):
#         self.customer = Customer.objects.create_user(email="customer@example.com", phone="09123456789", password="testpassword")
#         self.client = Client()
#         self.login_url = reverse('customers:login')
#         self.verify_url = reverse('customers:verify')
#         self.client.cookies['code'] = '123456'
#         self.client.cookies['user_id'] = str(self.customer.id)
#
#
#
#     def test_login_with_invalid_email(self):
#         data = {'login': 'invalid@example.com', 'password': 'testpassword'}
#         response = self.client.post(self.login_url, data)
#
#         self.assertEqual(response.status_code, 401)
#         self.assertNotIn('_auth_user_id', self.client.session)
#
#     def test_login_with_valid_phone(self):
#         data = {'login': '09123456789', 'password': 'testpassword'}
#         response = self.client.post(self.login_url, data)
#
#         # self.assertRedirects(response, self.verify_url)
#         self.assertIn('code', self.client.cookies)
#         self.assertIn('user_id', self.client.cookies)
#
#     def test_login_with_invalid_phone(self):
#         data = {'login': '09123456780', 'password': 'testpassword'}
#         response = self.client.post(self.login_url, data)
#
#         self.assertEqual(response.status_code, 401)
#         self.assertNotIn('_auth_user_id', self.client.session)
#
#


