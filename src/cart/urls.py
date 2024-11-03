
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import AddressAndOrderView,PurchaseView

app_name = 'cart'
urlpatterns = [
    path('api/v1/', include('cart.api.v1.urls')),
    path('shop/checkout/',AddressAndOrderView.as_view(), name='checkout'),
    path('purchase/',PurchaseView.as_view(), name='purchase_basket')

    # path('address/list/', AddressListView.as_view(), name='address-list'),
    # path('address/create/', AddressCreateView.as_view(), name='address-create'),
    # path('order/update/',OrderUpdateView.as_view(), name='order-update')

]


