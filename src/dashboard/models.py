from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import jdatetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import Address
from customers.models import Customer
from website.models import Product


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, null=True, blank=True, allow_unicode=True, verbose_name=_("Slug"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    order_count = models.IntegerField(default=0, verbose_name=_("Order Count"))
    rating_count = models.IntegerField(default=0, verbose_name=_("Rating Count"))
    sum_rating = models.IntegerField(default=0, verbose_name=_("Sum Rating"))
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=1.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        verbose_name=_("Average Rating")
    )
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='shop_address',
                                   verbose_name=_("Address"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            num = 1
            while Shop.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def persian_create_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.created_at).strftime('%Y-%m-%d')
        return persian_date

    def persian_update_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        return persian_date

    def update_average_rating(self):
        if self.rating_count > 0:
            self.average_rating = round(self.sum_rating / self.rating_count, 1)

    def __str__(self):
        return f"Shop Name: {self.name} (ID: {self.id})"


class ShopProduct(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("PERCENTAGE", _('Percentage Discount')),
        ("FIXED", _('Fixed Discount')),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_products', verbose_name=_('Shop'))
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='products',
                                   verbose_name=_('Product'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True,
        verbose_name=_("Discount")
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default="PERCENTAGE",
                                     verbose_name=_("Discount Type"))
    stock = models.IntegerField(default=0, blank=True, null=True, verbose_name=_("Stock"))
    rating_count = models.IntegerField(default=0, verbose_name=_("Rating Count"))
    sum_rating = models.IntegerField(default=0, verbose_name=_("Sum Rating"))
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=1.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        verbose_name=_("Average Rating")
    )

    def get_discounted_price(self):
        if self.discount_type == "PERCENTAGE":
            if self.discount:
                return self.price * (1 - self.discount / 100)
        elif self.discount_type == "FIXED":
            if self.discount:
                return max(self.price - self.discount, 0)
        return self.price

    def update_average_rating(self):
        if self.rating_count > 0:
            self.average_rating = round(self.sum_rating / self.rating_count, 1)

    def __str__(self):
        return f'{self.product.name} in {self.shop.name} with price {self.price} and discount {self.discount}'

    def get_absolute_url(self):
        return reverse('shop-product-detail', kwargs={'pk': self.pk})


class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("User"))
    rating = models.IntegerField(default=1,
                                 validators=[
                                     MinValueValidator(1),
                                     MaxValueValidator(5)
                                 ],
                                 verbose_name=_("Rating"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self.pk:
            old_rating = Rating.objects.get(pk=self.pk)
            self.content_object.sum_rating -= old_rating.rating
        else:
            self.content_object.rating_count += 1

        self.content_object.sum_rating += self.rating
        self.content_object.update_average_rating()
        self.content_object.save()
        super().save(*args, **kwargs)

    def persian_create_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.created_at).strftime('%Y-%m-%d %H:%M:%S')
        return persian_date

    def persian_update_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        return persian_date

    def __str__(self):
        return f'{self.user.email} rated {self.content_object} as {self.rating}'


class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, verbose_name=_("User"))
    ShopProduct = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='product_comments',
                                    verbose_name=_("Product"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    text = models.TextField(verbose_name=_("Text"))
    COMMENT_STATUS_CHOICES = [
        ("Submitted", _("Submitted")),
        ("Rejected", _("Rejected")),
        ("Approved", _("Approved")),
        ("Pending", _("Pending")),
    ]
    status = models.CharField(choices=COMMENT_STATUS_CHOICES, max_length=100, verbose_name=_("Status"),
                              default=COMMENT_STATUS_CHOICES[0][0])

    def persian_create_at(self):
        persian_date = jdatetime.date.fromgregorian(date=self.created_at).strftime('%Y-%m-%d')
        return persian_date

    def update_status(self, new_status):
        if new_status in dict(self.COMMENT_STATUS_CHOICES):
            self.status = new_status
            self.save()

    def __str__(self):
        return f"Comment: {self.text} by {self.user} on {self.ShopProduct.product} at {self.created_at}"
