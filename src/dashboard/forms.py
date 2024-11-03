from django import forms

from dashboard.models import Shop, ShopProduct, Rating
from django.utils.translation import gettext_lazy as _


# class ShopForm(forms.ModelForm):
#     class Meta:
#         model = Shop
#         fields = ['name', 'address']

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'slug']


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['price', 'discount', 'discount_type', 'stock']
        labels = {
            'price': _('قیمت'),
            'discount': _('تخفیف'),
            'discount_type': _('نوع تخفیف'),
            'stock': _('موجودی'),
        }
        help_texts = {
            'price': _('قیمت محصول را وارد کنید.'),
            'discount': _('مقدار تخفیف را وارد کنید (درصدی یا ثابت).'),
            'discount_type': _('نوع تخفیف را انتخاب کنید (درصدی یا ثابت).'),
            'stock': _('مقدار موجودی برای این محصول را وارد کنید.'),
        }


# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['rating']
#         widgets = {
#             'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
#         }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.HiddenInput(),
        }