import random
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormView, CreateView
from accounts.forms import AddressForm
from accounts.models import User
from cart.models import Order, ProductOrder
from customers.forms import VerifyPhoneCodeForm
from customers.views import send_sms_code
from dashboard.forms import ShopForm
from dashboard.models import ShopProduct, Comment
from .forms import StaffRegistrationForm, StaffLoginModelForm, CreateStaffForm, CommentStatusForm, OrderStatusForm
from .models import Staff


class StaffRegisterView(CreateView):
    model = Staff
    form_class = StaffRegistrationForm
    template_name = 'vendors/page-account-register.html'
    success_url = reverse_lazy('vendors:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['address_form'] = AddressForm(self.request.POST)
            context['shop_form'] = ShopForm(self.request.POST)
        else:
            context['address_form'] = AddressForm()
            context['shop_form'] = ShopForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_form = context['address_form']
        shop_form = context['shop_form']

        if form.is_valid() and address_form.is_valid() and shop_form.is_valid():
            address = address_form.save()
            shop = shop_form.save(commit=False)
            shop.address = address
            shop.save()

            staff = form.save(commit=False)
            staff.shop = shop
            staff.type = 'owner'
            staff.save()
            is_owner_permission = Permission.objects.get(codename='is_owner')
            is_manager_permission = Permission.objects.get(codename='is_manager')
            staff.user_permissions.add(is_owner_permission)
            staff.user_permissions.add(is_manager_permission)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StaffLoginView(FormView):
    template_name = 'vendors/page-account-login.html'
    form_class = StaffLoginModelForm

    def form_valid(self, form):
        login_field = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, login=login_field, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponse('Invalid login')

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page is not None:
            return redirect(next_page)
        return reverse_lazy('website:product-list')

class StaffLoginView(FormView):
    template_name = 'vendors/page-account-login.html'
    form_class = StaffLoginModelForm
    success_url = reverse_lazy('website:product-list')

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

                    self.request.session['code'] = code
                    self.request.session['authenticated_user_id'] = user.id
                    return redirect(reverse_lazy('vendors:verify'))

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
    template_name = 'accounts/verify2.html'
    form_class = VerifyPhoneCodeForm
    success_url = reverse_lazy('website:product-list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('code')
            session_code = self.request.session.get('code')
            user_id = self.request.session.get('authenticated_user_id')

            if session_code and int(entered_code) == session_code and user_id:
                user = User.objects.get(id=user_id)
                login(self.request, user, backend='accounts.backends.CustomBackend')
                del self.request.session['code']
                del self.request.session['authenticated_user_id']
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






def staff_context(request):
    if request.user.is_authenticated:
        try:
            staff = Staff.objects.get(id=request.user.id)
        except Staff.DoesNotExist:
            staff = None
    else:
        staff = None
    return {'staff': staff}


class CreateStaffView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Staff
    form_class = CreateStaffForm
    template_name = 'vendors/page-create-staff.html'
    success_url = reverse_lazy('vendors:register')
    permission_required = 'vendors.is_owner'
    raise_exception = True

    def form_valid(self, form):
        staff = form.save(commit=False)
        owner = Staff.objects.get(email=self.request.user.email)
        staff.shop = owner.shop
        staff.save()
        if staff.type == "manager":
            is_manager_permission = Permission.objects.get(codename='is_manager')
            staff.user_permissions.add(is_manager_permission)
        return super().form_valid(form)


# class CommentUpdateView(UpdateView):
#     model = Comment
#     fields = ['status']
#     template_name = 'vendors/comment.html'
#     context_object_name = 'comment'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         staff = Staff.objects.get(id=self.request.user.id)
#         shop = staff.shop
#         context['comments'] = Comment.objects.filter(ShopProduct__shop=shop)
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('comment_list')


class CommentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('vendors:login')
    permission_required = 'vendors.is_manager'
    model = Comment
    template_name = 'vendors/comment.html'
    context_object_name = 'comments'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = CommentStatusForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment_id']
            new_status = form.cleaned_data['status']
            comment = Comment.objects.get(id=comment_id)
            comment.update_status(new_status)
        return redirect(reverse_lazy('vendors:comment'))

    def get_queryset(self):
        staff = Staff.objects.get(id=self.request.user.id)
        shop = staff.shop
        return Comment.objects.filter(ShopProduct__shop=shop)


class CommentForSupervisorListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('vendors:login')
    model = Comment
    template_name = 'vendors/comment.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        staff = Staff.objects.get(id=self.request.user.id)
        shop = staff.shop
        return Comment.objects.filter(ShopProduct__shop=shop)


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('vendors:login')
    permission_required = 'vendors.is_manager'
    model = Order
    template_name = 'vendors/orders.html'
    # context_object_name = 'orders'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            new_delivered = form.cleaned_data['delivered']
            order = Order.objects.get(id=order_id)
            order.update_delivered(new_delivered)
        return redirect(reverse_lazy('vendors:orders'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = []
        staff = Staff.objects.get(id=self.request.user.id)
        shop = staff.shop
        product_orders = ProductOrder.objects.filter(product__shop=shop)
        for product_order in product_orders:
            order = product_order.order
            orders.append(order)
        set_orders = set(orders)
        context['orders'] = set_orders
        return context


class OrderForSupervisorListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('vendors:login')
    model = Order
    template_name = 'vendors/orders.html'
    # context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = []
        staff = Staff.objects.get(id=self.request.user.id)
        shop = staff.shop
        product_orders = ProductOrder.objects.filter(product__shop=shop)
        for product_order in product_orders:
            order = product_order.order
            orders.append(order)
        set_orders = set(orders)
        context['orders'] = set_orders
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('vendors:login')
    model = Order
    template_name = 'vendors/orders_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_orders'] = ProductOrder.objects.filter(order=self.get_object())
        return context

# class OrderListView(LoginRequiredMixin, ListView):
#     login_url = reverse_lazy('vendors:login')
#     model = Order
#     template_name = 'vendors/orders.html'
#     paginate_by = 10
#
#     def post(self, request, *args, **kwargs):
#         if request.user.has_perm('vendors.is_manager'):
#             form = OrderStatusForm(request.POST)
#             if form.is_valid():
#                 order_id = form.cleaned_data['order_id']
#                 new_delivered = form.cleaned_data['delivered']
#                 order = Order.objects.get(id=order_id)
#                 order.update_delivered(new_delivered)
#             return redirect(reverse_lazy('vendors:orders'))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         orders = []
#         staff = Staff.objects.get(id=self.request.user.id)
#         shop = staff.shop
#         product_orders = ProductOrder.objects.filter(product__shop=shop)
#         for product_order in product_orders:
#             order = product_order.order
#             orders.append(order)
#         set_orders = set(orders)
#         context['orders'] = set_orders
#
#         if self.request.user.has_perm('vendors.is_manager'):
#             context['is_manager'] = True
#         else:
#             context['is_manager'] = False
#
#         return context
