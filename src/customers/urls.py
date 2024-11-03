from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import CustomerRegisterView, CustomerLoginView, CustomerAndProfileUpdateView, AddressDeleteView, \
    AddressUpdateView, CustomPasswordChangeView,CodeVerificationView

app_name = 'customers'
urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('profile/', CustomerAndProfileUpdateView.as_view(), name='profile'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='delete_address'),
    path('address/<int:pk>/edit/', AddressUpdateView.as_view(), name='edit_address'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('verify/', CodeVerificationView.as_view(), name='verify')
    # path('verify-phone/', VerifyPhoneCodeView.as_view(), name='verify_phone_code'),

]

