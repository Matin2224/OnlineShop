from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from dashboard.views import ShopDetailView
from .views import CategoryCreateView, CategoryListView, ProductCreateView, \
    ShopProductUpdateView, ShopProductDeleteView, ShopProductDetailView, StaffAndShopProductView, \
    StaffDetailView, StaffUpdateView, StaffDeleteView, ShopUpdateView, ShopProductDetail, ShopListView, ShopDetailView, \
    CheapShopProductListView, ExpensiveShopProductListView, MostSellingShopProductListView,ShopAndProductSearchView,bestShopProductListView

app_name = 'website'
urlpatterns = [
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/list/', CategoryListView.as_view(template_name='website/page-categories.html'),
         name='category-list'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('ShopProduct/list/', StaffAndShopProductView.as_view(), name='product-list'),
    path('product/<int:pk>/update/', ShopProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ShopProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>/detail/', ShopProductDetailView.as_view(), name='product-detail'),
    path('staff/<int:pk>/update/', StaffUpdateView.as_view(), name='staff-update'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),
    path('staff/<int:pk>/detail/', StaffDetailView.as_view(), name='staff-detail'),
    path('shop/<int:pk>/update/', ShopUpdateView.as_view(), name='shop-update'),
    path('shop_product/<int:pk>/detail/', ShopProductDetail.as_view(), name='shop-product-detail'),
    path('shop_list/', ShopListView.as_view(), name='shop_list'),
    path('shop_detail/<int:pk>/', ShopDetailView.as_view(), name='shop_detail'),
    path('cheap_product/', CheapShopProductListView.as_view(), name='cheap_product'),
    path('expensive_product/', ExpensiveShopProductListView.as_view(), name='expensive_product'),
    path('most_selling_product/', MostSellingShopProductListView.as_view(), name='most_selling'),
    path('search/', ShopAndProductSearchView.as_view(), name='search'),
    path('best/',bestShopProductListView.as_view(), name='best')

]
