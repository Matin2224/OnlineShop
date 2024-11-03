from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import CombinedListView, ShopListView, ShopProductListView, ShopDetailView, \
    ShopProductDetailView, CategoryDetailView, CommentCreateView, NewestShopListView, ShopSortedByQuantityView, \
    RateProductView,RateShopView,BestShopView
from website.views import CategoryListView

# app_name = 'dashboard'
# urlpatterns = [
#     path('shop/', CombinedView.as_view(), name='shops')
#     # path('shop_product/', ShopProductListView.as_view(), name='shop-products'),
#     # path('category/list/', CategoryListView.as_view(template_name='website/index.html'), name='category-list'),
# ]

app_name = 'dashboard'

urlpatterns = [
    path('', CombinedListView.as_view(), name='combined-list'),
    path('shops/', ShopListView.as_view(), name='shops'),
    path('shop_products/', ShopProductListView.as_view(), name='shop-products'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('shop/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('shop_product/<int:pk>/', ShopProductDetailView.as_view(), name='shop-product-detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('comment/<int:pk>', CommentCreateView.as_view(), name='comment_create'),
    path('newest_shop/', NewestShopListView.as_view(), name='newest_shop_list'),
    path('top_selling/', ShopSortedByQuantityView.as_view(), name='top_selling'),
    path('rate/shop/<int:pk>/', RateShopView.as_view(), name='rate_shop'),
    path('rate/product/<int:pk>/',RateProductView.as_view(), name='rate_product'),
    path('best/shop/', BestShopView.as_view(), name='best')
]
