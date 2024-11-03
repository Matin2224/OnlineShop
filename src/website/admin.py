from django.contrib import admin

from .models import Product, Category, Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parents','slug')
    search_fields = ('name',)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('text', 'user', 'product', 'created_at')
#     search_fields = ('text', 'user', 'product')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'image')
    search_fields = ('content_object',)
