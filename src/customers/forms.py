import jdatetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Customer, CustomerProfile
from django.utils.translation import gettext_lazy as _


class CustomerRegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
        strip=False,
        help_text=_("Your password must contain at least 8 characters."),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(),
        strip=False,
        help_text=_("Enter the same password as above."),
    )

    # birthdate = forms.DateField(
    #     label=_("Birth Date"),
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     help_text=_("Enter your birth date in the format YYYY-MM-DD."),
    # )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
        labels = {
            'password1': _('Password'),
            'password2': _('Confirm Password'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email Address'),
            'phone': _('Phone'),
            'birthdate': _('Birth Date')
        }
        help_texts = {
            'phone': _('Phone number should be 11 digits long.')
        }

    # def clean_birthdate(self):
    #     birthdate = self.cleaned_data.get('birthdate')
    #     if not birthdate:
    #         return birthdate
    #
    #     try:
    #         jalali_date = jdatetime.datetime.strptime(birthdate, '%Y/%m/%d')
    #         # Convert to Gregorian date
    #         gregorian_date = jalali_date.togregorian()
    #         return gregorian_date
    #     except ValueError:
    #         raise ValidationError(_('Invalid birthdate format. Use YYYY-MM-DD.'))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("The two password fields must match."))

        return cleaned_data


#
# class CustomerLoginModelForm(forms.Form):
#     login = forms.CharField(
#         error_messages={
#             'required': 'وارد کردن این فیلد الزامی است.',
#             'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
#         }
#     )
#     password = forms.CharField(
#         error_messages={
#             'required': 'وارد کردن این فیلد الزامی است.',
#             'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
#         }
#     )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['bio', 'profile_image']


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label=_("رمز عبور فعلی"))
    new_password1 = forms.CharField(label=_("رمز عبور جدید"))
    new_password2 = forms.CharField(label=_("تأیید رمز عبور"))

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("رمزهای عبور جدید یکسان نیستند."))

        return cleaned_data


class VerifyPhoneCodeForm(forms.Form):
    code = forms.CharField(max_length=6, label=' کد تایید')


class CustomerLoginModelForm(forms.Form):
    login = forms.CharField(
        label='Phone or Email',
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Phone or Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
