

from django import forms
from django.forms import inlineformset_factory

from accounts.forms import AddressForm
from accounts.models import Address
from cart.models import Order
from dashboard.forms import ShopForm
from dashboard.models import Shop, Comment
from vendors.models import Staff


class StaffRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))


    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords must match.")
        return cleaned_data

    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.set_password(self.cleaned_data['password1'])
        staff.type = 'owner'
        if commit:
            staff.save()
        return staff


class StaffLoginModelForm(forms.Form):
    login = forms.CharField(
        error_messages={
            'required': 'وارد کردن این فیلد الزامی است.',
            'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
        }
    )
    password = forms.CharField(
        error_messages={
            'required': 'وارد کردن این فیلد الزامی است.',
            'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
        }
    )


class CreateStaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    type = forms.ChoiceField(choices=[('operator', 'Operator'), ('manager', 'Manager')],
                             required=True, widget=forms.Select(attrs={'placeholder': 'Type'}))

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'type']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords must match.")
        return cleaned_data

    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.set_password(self.cleaned_data['password1'])
        if commit:
            staff.save()
        return staff


class CommentStatusForm(forms.Form):
    comment_id = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=Comment.COMMENT_STATUS_CHOICES)


class OrderStatusForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())
    delivered = forms.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)