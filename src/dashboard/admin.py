from django.contrib import admin

from .models import Shop, Rating, ShopProduct, Comment


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'address')
    search_fields = ('name',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating')
    search_fields = ('user', 'content_object')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'discount')
    search_fields = ('shop', 'product')
    list_filter = ('shop',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'ShopProduct', 'created_at')
    search_fields = ('text', 'user', 'ShopProduct')
