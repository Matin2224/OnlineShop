from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView
from django.views.generic.edit import CreateView

from dashboard.forms import ShopProductForm
from dashboard.models import ShopProduct, Shop, Comment
from vendors.models import Staff
from .models import Category, Product
from .forms import CategoryForm, ImageForm, ProductForm, ShopProductUpdateForm, StaffUpdateForm


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    raise_exception = True


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'website/page-categories.html'
    success_url = reverse_lazy('website:category-create')
    permission_required = 'vendors.is_manager'
    raise_exception = True

    def form_valid(self, form):
        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'website/page-form-product.html'
    success_url = reverse_lazy('website:product-create')
    permission_required = 'vendors.is_manager'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['shop_product_form'] = ShopProductForm(self.request.POST)
            context['image_form'] = ImageForm(self.request.POST, self.request.FILES)
        else:
            context['categories'] = Category.objects.all()
            context['shop_product_form'] = ShopProductForm()
            context['image_form'] = ImageForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        shop_product_form = context['shop_product_form']
        image_form = context['image_form']

        if form.is_valid() and shop_product_form.is_valid() and image_form.is_valid():
            product = form.save()

            shop_product = shop_product_form.save(commit=False)
            shop_product.product = product
            owner = Staff.objects.get(email=self.request.user.email)
            shop_product.shop = owner.shop
            shop_product.save()

            image = image_form.save(commit=False)
            image.content_object = product
            image.save()

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


# class StaffShopProductListView(LoginRequiredMixin, ListView):
#     model = ShopProduct
#     template_name = 'vendors/index.html'
#     context_object_name = 'shop_products'
#
#     def get_queryset(self):
#         staff = Staff.objects.get(id=self.request.user.id)
#         shop = staff.shop
#         return ShopProduct.objects.filter(shop=shop)


class ShopProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'vendors.is_manager'
    model = ShopProduct
    context_object_name = 'product'
    form_class = ShopProductUpdateForm
    template_name = 'vendors/product-update.html'

    def get_queryset(self):
        shop = self.request.user.staff.shop
        return ShopProduct.objects.filter(shop=shop)

    def get_success_url(self):
        return reverse_lazy('website:product-detail', kwargs={'pk': self.object.pk})


class ShopProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'vendors.is_manager'
    model = ShopProduct
    template_name = 'vendors/product-delete.html'

    success_url = reverse_lazy('vendors:register')

    def get_queryset(self):
        shop = self.request.user.staff.shop
        return ShopProduct.objects.filter(shop=shop)


class ShopProductDetailView(LoginRequiredMixin, DetailView):
    model = ShopProduct
    template_name = 'vendors/product-detail.html'
    context_object_name = 'shop_product'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'staff'):
            return ShopProduct.objects.filter(shop=user.staff.shop)
        return ShopProduct.objects.none()


# class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     permission_required = 'vendors.is_owner'
#     model = Staff
#     template_name = 'vendors/index.html'
#     context_object_name = 'staffs'
#
#     def get_queryset(self):
#         staff = Staff.objects.get(id=self.request.user.id)
#         shop = staff.shop
#         return Staff.objects.filter(shop=shop)


class StaffAndShopProductView(LoginRequiredMixin, TemplateView):
    # permission_required = 'vendors.is_owner'
    template_name = 'vendors/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = Staff.objects.get(id=self.request.user.id)
        shop = staff.shop
        context['staffs'] = Staff.objects.filter(shop=shop)
        context['shop_products'] = ShopProduct.objects.filter(shop=shop)
        # context['comments'] = Comment.objects.filter(ShopProduct__shop=shop)
        return context


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'vendors.is_owner'
    model = Staff
    template_name = 'vendors/staff-detail.html'
    context_object_name = 'staff'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'staff'):
            return Staff.objects.filter(shop=user.staff.shop)
        return Staff.objects.none()


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'vendors.is_owner'
    model = Staff
    form_class = StaffUpdateForm
    template_name = 'vendors/staff-update.html'

    def get_queryset(self):
        shop = self.request.user.staff.shop
        return Staff.objects.filter(shop=shop)

    def get_success_url(self):
        return reverse_lazy('website:staff-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password')

        if old_password and new_password:
            if self.object.check_password(old_password):
                self.object.set_password(new_password)
                self.object.save()
                update_session_auth_hash(self.request, self.object)
            else:
                form.add_error('old_password', 'رمز عبور قبلی نادرست است.')
                return self.form_invalid(form)

        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'vendors.is_owner'
    model = Staff
    template_name = 'vendors/staff-delete.html'
    success_url = reverse_lazy('vendors:register')

    def get_queryset(self):
        shop = self.request.user.staff.shop
        return Staff.objects.filter(shop=shop)


class ShopUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'vendors.is_owner'
    model = Shop
    fields = ['name', 'active', 'address']
    template_name = 'vendors/shop-update.html'
    success_url = reverse_lazy('website:product-list')

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'staff'):
            return Shop.objects.filter(id=user.staff.shop.id)
        return Shop.objects.none()


class ShopProductDetail(DetailView):
    model = ShopProduct
    template_name = 'website/shop-product-full.html'
    context_object_name = 'shop_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop_product = self.get_object()

        context['product_name'] = shop_product.product.name
        context['price_before_discount'] = shop_product.price
        context['price_after_discount'] = shop_product.get_discounted_price()
        context['discount_type'] = shop_product.get_discount_type_display()
        context['stock'] = shop_product.stock
        context['properties'] = shop_product.product.properties
        context['image_url'] = shop_product.product.get_image_url()
        context['comment_create_url'] = reverse_lazy('dashboard:comment_create', kwargs={'pk': shop_product.id})
        context['comments'] = Comment.objects.filter(ShopProduct=shop_product, status="Approved")
        context['count_comment'] = len(context['comments'])
        return context


# class CommentUpdateView(UserPassesTestMixin, UpdateView):
#     model = Comment
#     fields = ['status']
#     template_name = 'comments/comment_status_form.html'
#     success_url = reverse_lazy('comment-list')  # Redirect to a success page or list view
#
#     def test_func(self):
#         user = self.request.user
#         return user.is_staff  # Ensure the user is a staff member
#
#     def form_valid(self, form):
#         return super().form_valid(form)


class ShopListView(ListView):
    model = Shop
    template_name = 'website/shops.html'
    context_object_name = 'shops'
    paginate_by = 10

    def get_queryset(self):
        return Shop.objects.filter(active=True)


class ShopDetailView(DetailView):
    model = Shop
    template_name = 'website/shops_details.html'
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['shop_products'] = self.object.shop_products.all()
        context['shop_products'] = ShopProduct.objects.filter(shop=self.get_object())
        return context


class ExpensiveShopProductListView(ListView):
    model = ShopProduct
    template_name = 'website/index.html'
    context_object_name = 'shop_products'
    ordering = ['price']

    def get_queryset(self):
        queryset = ShopProduct.objects.all()
        queryset = sorted(queryset, key=lambda product: product.get_discounted_price(), reverse=True)
        return queryset


class CheapShopProductListView(ListView):
    model = ShopProduct
    template_name = 'website/index.html'
    context_object_name = 'shop_products'
    ordering = ['price']

    def get_queryset(self):
        queryset = ShopProduct.objects.all()
        queryset = sorted(queryset, key=lambda obj: obj.get_discounted_price())
        return queryset


class MostSellingShopProductListView(ListView):
    model = ShopProduct
    template_name = 'website/index.html'
    context_object_name = 'shop_products'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            total_quantity=Sum('productorder__quantity')
        ).order_by('-total_quantity')
        return queryset


class ShopAndProductSearchView(ListView):
    template_name = 'website/index.html'
    context_object_name = 'obj'

    def get_queryset(self):
        query = self.request.GET.get('q')
        shop_results = []
        product_results = []

        if query:
            shop_results = Shop.objects.filter(name__icontains=query)

            product_results = ShopProduct.objects.filter(product__name__icontains=query)

        context = {
            'shops_result': shop_results,
            'products_result': product_results
        }

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

#
# class ShopAndProductSearchView(ListView):
#     template_name = 'website/index.html'
#     context_object_name = 'obj'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         context = {}
#
#         if query:
#             # Elasticsearch search for shops
#             shop_results = ShopDocument.search().query("multi_match", query=query, fields=['name']).to_queryset()
#
#             # Elasticsearch search for products using the correct 'product_name' field
#             product_results = ShopProductDocument.search().query("multi_match", query=query, fields=['product_name']).to_queryset()
#
#             context = {
#                 'shops_result': shop_results,
#                 'products_result': product_results
#             }
#
#         return context
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['query'] = self.request.GET.get('q', '')
#         return context

class bestShopProductListView(ListView):
    model = ShopProduct
    template_name = 'website/index.html'
    context_object_name = 'shop_products'
    ordering = ['-average_rating']

