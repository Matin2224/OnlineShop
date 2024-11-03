from django.contrib import admin
from .models import Customer, CustomerProfile

admin.site.register(Customer)

# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ("['address']")
#     search_fields = (['address'])
admin.site.register(CustomerProfile)

# @admin.register(CustomerProfile)
# class CustomerProfileAdmin(admin.ModelAdmin):
#     list_display = ('customers', 'profile_image')
#     search_fields = ('customers',)
