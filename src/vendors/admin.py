from django.contrib import admin

from .models import StaffProfile, Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('type', 'shop')
    search_fields = ('type',)
    list_filter = ('type', 'shop')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
