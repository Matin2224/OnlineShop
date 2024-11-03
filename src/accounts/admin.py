from django.contrib import admin

from django.contrib import admin
from .models import Address, User, Profile


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'zipcode')
    search_fields = ('street', 'city', 'state', 'zipcode')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'birthdate')
    search_fields = ('email', 'phone')
    list_filter = ('birthdate',)


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'bio', 'profile_image')
#     search_fields = ('user', 'bio')
