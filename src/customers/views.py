import json
import random
import re

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from melipayamak import Api

import requests
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from accounts.forms import AddressForm

from cart.api.v1.views import CreateOrderView
from cart.models import Order, ProductOrder
from dashboard.models import Comment, Shop, ShopProduct, Rating
from .forms import CustomerForm, ProfileForm, CustomPasswordChangeForm, VerifyPhoneCodeForm
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from accounts.backends import *
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from accounts.models import Address, User
from .forms import CustomerRegisterModelForm, CustomerLoginModelForm
from .models import Customer, CustomerProfile
import redis


class CustomerRegisterView(CreateView):
    model = Customer
    form_class = CustomerRegisterModelForm
    template_name = 'accounts/page-login-register.html'
    success_url = reverse_lazy('customers:register')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user, backend='accounts.backends.CustomBackend')
        return response

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


def send_sms_code(code, phone):
    username = "09303204925"
    password = "@Y#LH"
    api = Api(username, password)
    sms = api.sms()
    to = phone
    _from = '50002710004925'
    text = f'Your verification code is  {code}   '
    response = sms.send(to, _from, text)
    return response


class CustomerLoginView(FormView):
    template_name = 'accounts/page-login-register.html'
    form_class = CustomerLoginModelForm
    success_url = reverse_lazy('customers:profile')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        next_page = request.GET.get('next', '')
        context = self.get_context_data(form=form, next=next_page)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            login_field = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request=self.request, login=login_field, password=password)

            if user is not None:
                regex = r'^(09)\d{9}$'
                if re.match(regex, login_field):
                    code = random.randint(100000, 999999)
                    send_sms_code(code, user.phone)
                    # print(f"Generated Code: {code}")
                    cache.set("code", code, timeout=300)
                    cache.set('authenticated_user_id', user.id, timeout=300)
                    # self.request.session['code'] = code
                    # self.request.session['authenticated_user_id'] = user.id
                    return redirect(reverse_lazy('customers:verify'))

                else:
                    login(self.request, user, backend='accounts.backends.CustomBackend')
                    next_page = self.request.POST.get('next', '')
                    if not next_page:
                        next_page = self.request.GET.get('next', '')
                    if next_page:
                        return redirect(next_page)
                    return super().form_valid(form)
            else:
                return HttpResponse('Invalid login', status=401)
        else:
            return self.form_invalid(form)


class CodeVerificationView(FormView):
    template_name = 'accounts/verify.html'
    form_class = VerifyPhoneCodeForm
    success_url = reverse_lazy('customers:profile')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('code')
            session_code = cache.get('code')
            user_id = cache.get('authenticated_user_id')
            # session_code = self.request.session.get('code')
            # user_id = self.request.session.get('authenticated_user_id')

            if session_code and int(entered_code) == session_code and user_id:
                user = User.objects.get(id=user_id)
                login(self.request, user, backend='accounts.backends.CustomBackend')
                cache.delete('code')
                cache.delete('authenticated_user_id')
                # del self.request.session['code']
                # del self.request.session['authenticated_user_id']
                next_page = self.request.POST.get('next', '')
                if not next_page:
                    next_page = self.request.GET.get('next', '')
                if next_page:
                    return redirect(next_page)
                return super().form_valid(form)
            else:
                form.add_error('code', 'Invalid verification code')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


# class CodeVerificationView(FormView):
#     template_name = 'accounts/verify.html'
#     form_class = VerifyPhoneCodeForm
#     success_url = reverse_lazy('customers:profile')
#
#     def form_valid(self, form):
#         entered_code = form.cleaned_data.get('code')
#         session_code = self.request.COOKIES.get('code')
#         user_id = self.request.COOKIES.get('user_id')
#
#         if self.is_code_valid(entered_code, session_code) and user_id:
#             return self.log_user_in(form, user_id)
#         else:
#             form.add_error('code', 'Invalid verification code')
#             return self.form_invalid(form)
#
#     def is_code_valid(self, entered_code, session_code):
#         return session_code and int(entered_code) == int(session_code)
#
#     def log_user_in(self, form, user_id):
#         user = User.objects.get(id=user_id)
#         login(self.request, user, backend='accounts.backends.CustomBackend')
#
#         response = self.clear_verification_cookies(super().form_valid(form))
#         return self.redirect_to_next_or_profile(response)
#
#     def clear_verification_cookies(self, response):
#         response.delete_cookie('code')
#         response.delete_cookie('user_id')
#         return response
#
#     def redirect_to_next_or_profile(self, response):
#         next_page = self.request.POST.get('next', '') or self.request.GET.get('next', '')
#         if next_page:
#             return redirect(next_page)
#         return response
#
#
# class CustomerLoginView(FormView):
#     template_name = 'accounts/page-login-register.html'
#     form_class = CustomerLoginModelForm
#     success_url = reverse_lazy('customers:profile')
#
#     def form_valid(self, form):
#         login_field = form.cleaned_data.get('login')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request=self.request, login=login_field, password=password)
#
#         if user:
#             if self.is_phone_number(login_field):
#                 return self.handle_phone_login(user)
#             else:
#                 return self.handle_email_login(user, form)
#         else:
#             return HttpResponse('Invalid login', status=401)
#
#     def is_phone_number(self, login_field):
#         regex = r'^(09)\d{9}$'
#         return re.match(regex, login_field) is not None
#
#     def handle_phone_login(self, user):
#         code = self.generate_verification_code()
#         send_sms_code(code, user.phone)
#
#         response = redirect(reverse_lazy('customers:verify'))
#         self.set_verification_cookies(response, code, user.id)
#         return response
#
#     def handle_email_login(self, user, form):
#         login(self.request, user, backend='accounts.backends.CustomBackend')
#         return self.redirect_to_next_or_profile(form)
#
#     def generate_verification_code(self):
#         return random.randint(100000, 999999)
#
#     def set_verification_cookies(self, response, code, user_id):
#         response.set_cookie('code', code, max_age=300)
#         response.set_cookie('user_id', user_id, max_age=300)
#
#     def redirect_to_next_or_profile(self, form):
#         next_page = self.request.POST.get('next', '') or self.request.GET.get('next', '')
#         if next_page:
#             return redirect(next_page)
#         return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('customers:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'customers/page-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if hasattr(user, 'customer'):
            customer = user.customer
            context['customer'] = customer
            context['addresses'] = customer.address.all()


        else:
            context['customer'] = None
            context['addresses'] = []

        # context['orders'] = []

        return context


class CustomerAndProfileUpdateView(View):
    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        customer_form = CustomerForm(instance=customer)
        profile_form = ProfileForm(instance=customer.customer_profile)
        addresses = customer.address.all()
        address_form = AddressForm()
        orders = Order.objects.filter(customer=customer).order_by('-create_at')
        products_orders = ProductOrder.objects.filter(order__in=orders).all()
        comments = Comment.objects.filter(user=customer).order_by('-created_at')
        orders_completed = Order.objects.filter(customer=customer, delivered='Completed')
        products_completed = ProductOrder.objects.filter(order__in=orders_completed).select_related('product').all()
        shop_ids = products_completed.values_list('product__shop', flat=True).distinct()
        shops = Shop.objects.filter(id__in=shop_ids)

        context = {
            'customer_form': customer_form,
            'profile_form': profile_form,
            'addresses': addresses,
            'address_form': address_form,
            'orders': orders,
            'products_orders': products_orders,
            'comments': comments,
            'shops': shops,
            'products_completed': products_completed
        }
        return render(request, 'customers/page-account.html', context)

    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        if request.POST:
            customer_form = CustomerForm(request.POST, instance=customer)
            profile_form = ProfileForm(request.POST, request.FILES, instance=customer.customer_profile)
            if customer_form.is_valid() and profile_form.is_valid():
                customer_form.save()
                profile_form.save()
                return redirect('customers:profile')

        if 'address_submit' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save()
                customer.address.add(address)
                customer.save()
                return redirect('customers:profile')

        addresses = customer.address.all()
        context = {
            'customer_form': CustomerForm(instance=customer),
            'profile_form': ProfileForm(instance=customer.customer_profile),
            'addresses': addresses,
            'address_form': AddressForm(),
        }
        return render(request, 'customers/page-account.html', context)


class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'customers/address_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('customers:profile')

    def get_object(self):
        address = super().get_object()
        customer = self.request.user.customer
        if address not in customer.address.all():
            raise Http404
        return address

    def delete(self, request, *args, **kwargs):
        customer = request.user.customer
        address = self.get_object()
        customer.address.remove(address)
        if not Address.objects.filter(customer_address__id=customer.id).exists():
            address.delete()
        return redirect(self.get_success_url())


class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'customers/address_form.html'

    def get_success_url(self):
        return reverse_lazy('customers:profile')

    def get_object(self):
        address = super().get_object()
        customer = self.request.user.customer
        if address not in customer.address.all():
            raise Http404
        return address


class CustomPasswordChangeView(FormView):
    template_name = 'customers/page-account.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('customers:profile')

    def form_valid(self, form):
        old_password = form.cleaned_data.get('old_password')
        new_password1 = form.cleaned_data.get('new_password1')
        user = self.request.user

        if not user.check_password(old_password):
            form.add_error('old_password', _("رمز عبور فعلی نادرست است."))
            return self.form_invalid(form)

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, _('رمز عبور شما با موفقیت تغییر کرد.'))
        return super().form_valid(form)
