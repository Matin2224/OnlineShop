from django.contrib import admin
from django.urls import path, include
from .views import StaffRegisterView, StaffLoginView, CreateStaffView, CommentListView, CommentForSupervisorListView, \
    OrderListView,OrderDetailView,\
    OrderForSupervisorListView,CodeVerificationView


app_name = 'vendors'
urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='login'),
    path('register/', StaffRegisterView.as_view(), name='register'),
    path('register_staff/', CreateStaffView.as_view(), name='create_staff'),
    path('comment/', CommentListView.as_view(), name='comment'),
    path('comment_s/', CommentForSupervisorListView.as_view(), name='comment_s'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders_s/', OrderForSupervisorListView.as_view(), name='orders_s'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('verify/', CodeVerificationView.as_view(), name='verify')

]
