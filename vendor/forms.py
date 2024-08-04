from django import forms 

from vendor.models import Vendor


class RegisterVendor(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

        widgets = {
            'vendor_name': forms.TextInput(attrs={'class':'form-control my-5', 'placeholder':'myrestaurant'}),
            'vendor_license': forms.FileInput(attrs={'class':'form-control my-5'}),
        }
