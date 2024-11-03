from django import forms

from accounts.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zipcode']
        labels = {
            'street': 'خیابان',
            'city': 'شهر',
            'state': 'استان',
            'zipcode': 'کد پستی',
        }
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control square'}),
            'city': forms.TextInput(attrs={'class': 'form-control square'}),
            'state': forms.TextInput(attrs={'class': 'form-control square'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control square'}),
        }
