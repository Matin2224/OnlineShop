from django.urls import path
from .views import CreateOrderView

app_name = 'api-v1'

urlpatterns = [
    path('orders/', CreateOrderView.as_view(), name='create-order'),
]
