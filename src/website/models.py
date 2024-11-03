from django.utils.translation import gettext_lazy as _

import jdatetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from customers.models import Customer
# from dashboard.models import ShopProduct



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, null=True, blank=True, verbose_name=_("Slug"))
    parents = models.ForeignKey("self", on_delete=models.CASCADE, related_name="parent_categories",
                                verbose_name=_("parents"), null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    # def get_subcategories(self):
    #     if self.subcategories:
    #         return ", ".join([subcategory.name for subcategory in self.subcategories])
    #     return ""

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, null=True, blank=True, allow_unicode=True, verbose_name=_("Slug"))
    properties = models.TextField(blank=True, null=True, verbose_name=_("Properties"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category',
                                 verbose_name=_("Category"))
    rating_count = models.IntegerField(default=0, verbose_name=_("Rating Count"))
    sum_rating = models.IntegerField(default=0, verbose_name=_("Sum Rating"))
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        default=1.0,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ],
        verbose_name=_("Average Rating")
    )

    def get_image_url(self):
        image = Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).first()
        if image:
            return image.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def update_average_rating(self):
        if self.rating_count > 0:
            self.average_rating = round(self.sum_rating / self.rating_count, 1)

    def __str__(self):
        return f"Product: {self.name}, Properties: {self.properties}, Average Rating: {self.average_rating},Category : {self.category}"


class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='default.jpg',
                              verbose_name=_("Image"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Object ID"))
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Image for {self.content_object}"
