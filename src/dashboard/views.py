# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView

from cart.models import Order
from dashboard.forms import RatingForm
from dashboard.models import Shop, ShopProduct, Comment, Rating
from website.models import Category


# class ShopListView(ListView):
#     model = Shop
#     template_name = 'website/index.html'
#     context_object_name = 'shops'
#
#
# class ShopProductListView(ListView):
#     model = ShopProduct
#     template_name = 'website/index.html'
#     context_object_name = 'ShopProducts'
#     paginate_by = 10
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sort_by = self.request.GET.get('sort_by', 'default')
#         if sort_by == 'bestselling':
#             queryset = queryset.order_by('-shop__order_count')
#         elif sort_by == 'highest_rated':
#             queryset = queryset.order_by('-shop__average_rating')
#         elif sort_by == 'most_expensive':
#             queryset = queryset.order_by('-price')
#
#         else:
#             queryset = queryset.order_by('product__name')
#
#         return queryset
# class CombinedView(View):
#     template_name = 'website/index.html'
#
#     def get(self, request, *args, **kwargs):
#         # Get context data from ShopListView
#         shops = Shop.objects.all()
#
#         # Get context data from ShopProductListView with sorting
#         sort_by = request.GET.get('sort_by', 'default')
#         shop_products = ShopProduct.objects.all()
#         if sort_by == 'bestselling':
#             shop_products = shop_products.order_by('-shop__order_count')
#         elif sort_by == 'highest_rated':
#             shop_products = shop_products.order_by('-shop__average_rating')
#         elif sort_by == 'most_expensive':
#             shop_products = shop_products.order_by('-price')
#         else:
#             shop_products = shop_products.order_by('product__name')
#
#         # Get context data from CategoryListView
#         categories = Category.objects.all()
#
#         # Combine all context data
#         context = {
#             'shops': shops,
#             'ShopProducts': shop_products,
#             'categories': categories,
#         }
#
#         return render(request, self.template_name, context)


# Combined View that shows Shops, ShopProducts, and Categories
class CombinedListView(ListView):
    template_name = 'website/index.html'
    context_object_name = 'data'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        context['shop_products'] = ShopProduct.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ShopListView(ListView):
    model = Shop
    template_name = 'website/shop-product-full.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.all()


# Shop Product List View
class ShopProductListView(ListView):
    model = ShopProduct
    template_name = 'website/shop_product_list.html'
    context_object_name = 'shop_products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'default')
        if sort_by == 'bestselling':
            queryset = queryset.order_by('-shop__order_count')
        elif sort_by == 'highest_rated':
            queryset = queryset.order_by('-shop__average_rating')
        elif sort_by == 'most_expensive':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('product__name')
        return queryset


# Category List View
class CategoryListView(ListView):
    model = Category
    template_name = 'website/category_list.html'
    context_object_name = 'categories'


# Detail Views for Shops, ShopProducts, and Categories
class ShopDetailView(DetailView):
    model = Shop
    template_name = 'website/shop_detail.html'
    context_object_name = 'shop'


class ShopProductDetailView(DetailView):
    model = ShopProduct
    template_name = 'website/shop_product_detail.html'
    context_object_name = 'shop_product'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'website/index.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['shop_products'] = ShopProduct.objects.filter(product__category_id=self.kwargs['pk'])
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'dashboard/comment.html'
    login_url = reverse_lazy('customers:login')

    def form_valid(self, form):
        shop_product = get_object_or_404(ShopProduct, pk=self.kwargs['pk'])
        form.instance.ShopProduct = shop_product
        form.instance.user = self.request.user.customer

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('website:shop-product-detail', kwargs={'pk': self.object.ShopProduct.pk})


class NewestShopListView(ListView):
    model = Shop
    template_name = 'website/shops.html'
    context_object_name = 'shops'
    ordering = ['-created_at']


class ShopSortedByQuantityView(ListView):
    model = Shop
    template_name = 'website/shops.html'
    context_object_name = 'shops'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            total_quantity=Sum('shop_products__productorder__quantity')
        ).order_by('-total_quantity')
        return queryset

class BestShopView(ListView):
    model = Shop
    template_name = 'website/shops.html'
    context_object_name = 'shops'
    ordering = ['-average_rating']


class RateProductView(LoginRequiredMixin, FormView):
    form_class = RatingForm
    template_name = 'customers/page-account.html'
    login_url = reverse_lazy('customers:login')

    def form_valid(self, form):
        rating = form.cleaned_data['rating']
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(ShopProduct, pk=product_id)

        content_type = ContentType.objects.get_for_model(product)
        rating_instance, created = Rating.objects.get_or_create(
            user=self.request.user.customer,
            content_type=content_type,
            object_id=product.id,
        )
        rating_instance.rating = rating
        rating_instance.save()

        return redirect('customers:profile')


class RateShopView(LoginRequiredMixin, FormView):
    form_class = RatingForm
    template_name = 'customers/page-account.html'
    login_url = reverse_lazy('customers:login')

    def form_valid(self, form):
        rating = form.cleaned_data['rating']
        shop_id = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, pk=shop_id)

        content_type = ContentType.objects.get_for_model(shop)
        rating_instance, created = Rating.objects.get_or_create(
            user=self.request.user.customer,
            content_type=content_type,
            object_id=shop.id,
        )
        rating_instance.rating = rating
        rating_instance.save()

        return redirect('customers:profile')
