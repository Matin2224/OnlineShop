# from django.contrib import admin
#
#
#
# from django.contrib.admin import AdminSite
#
# from accounts.models import User
# from customers.models import Customer
#
#
# class MyAdminSite(AdminSite):
#     site_header = 'بهترین انتخاب'
#     site_title = 'پنل ادمین'
#     index_title = 'به پنل فروشگاه خوش آمدید'
#
#
# admin_site = MyAdminSite(name='admin')
#
#
# from django.apps import apps
# from django.contrib import admin
# from .admin import admin_site  # Import your custom admin site
#
# # Loop through all the apps and register each model automatically
# for model in apps.get_models():
#     try:
#         admin_site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass  # If a model is already registered, skip it
