from django import forms

from dashboard.models import ShopProduct, Shop
from vendors.models import Staff
from .models import Category, Product, Image

from django import forms
from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parents', 'description']
        labels = {
            'name': _('نام دسته‌بندی'),
            'slug': _('اسلاگ دسته‌بندی'),
            'parents': _('والدین'),
            'description': _('توضیحات'),
        }
        error_messages = {
            'name': {
                'required': _('لطفاً نام دسته‌بندی را وارد کنید.'),
                'max_length': _('نام دسته‌بندی نمی‌تواند بیشتر از 100 کاراکتر باشد.'),
            },
            'slug': {
                'required': _('لطفاً اسلاگ دسته‌بندی را وارد کنید.'),
                'invalid': _('اسلاگ دسته‌بندی وارد شده معتبر نیست.'),
            },
            'parents': {
                'invalid_choice': _('لطفاً یک والد معتبر انتخاب کنید.'),
            },
            'description': {
                'required': _('لطفاً توضیحات را وارد کنید.'),
            },
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'properties', 'category']
        labels = {
            'name': _('نام محصول'),
            'slug': _('اسلاگ'),
            'properties': _('ویژگی‌ها'),
            'category': _('دسته بندی'),
        }
        help_texts = {
            'name': _('نام محصول را وارد کنید.'),
            'slug': _('اسلاگ محصول را وارد کنید. اگر خالی بگذارید به صورت خودکار تولید خواهد شد.'),
            'properties': _('ویژگی‌های اضافی محصول را به صورت فرمت JSON وارد کنید.'),
            'category': _('دسته بندی که این محصول به آن تعلق دارد را انتخاب کنید.'),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        labels = {
            'image': _('تصویر محصول'),
        }
        help_texts = {
            'image': _('تصویری برای محصول بارگذاری کنید.'),
        }


class ShopProductUpdateForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['price', 'discount', 'discount_type', 'stock']
        labels = {
            'price': 'قیمت',
            'discount': 'تخفیف',
            'discount_type': 'نوع تخفیف',
            'stock': 'موجودی',
        }
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'قیمت محصول را وارد کنید'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تخفیف محصول را وارد کنید'}),
            'discount_type': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'موجودی محصول را وارد کنید'}),
        }


class StaffUpdateForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور قبلی'}),
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور جدید'}),
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'تایید رمز عبور جدید'}),
        required=False
    )

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if old_password or new_password or confirm_password:
            if not old_password:
                self.add_error('old_password', 'رمز عبور قبلی مورد نیاز است.')
            if not new_password:
                self.add_error('new_password', 'رمز عبور جدید مورد نیاز است.')
            if new_password != confirm_password:
                self.add_error('confirm_password', 'تایید رمز عبور جدید مطابقت ندارد.')

        return cleaned_data


