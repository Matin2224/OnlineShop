
from django.contrib import admin
# from django.urls import path, include
#
#
# urlpatterns = [
#
#     path('accounts/',),
# ]

from django.contrib import admin
from django.urls import path, include
from .views import LogoutView, change_language
from django.conf.urls.i18n import set_language

app_name = 'accounts'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
