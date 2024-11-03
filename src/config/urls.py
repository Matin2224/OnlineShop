"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from accounts.views import change_language

# from config.admin import admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('customers/', include('customers.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('vendors/', include('vendors.urls')),
    path('website/', include('website.urls')),
    path('change-language/<str:lang_code>/', change_language, name='change_language')


    # path('api-auth/', include('rest_framework.urls'))
]


admin.site.site_header = 'بهترین انتخاب'
admin.site.site_title = 'پنل ادمین'
admin.site.index_title = 'به پنل فروشگاه خوش آمدید'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
