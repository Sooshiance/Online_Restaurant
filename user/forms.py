from django import forms

from user.models import User


class Register(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-5', 'placeholder':'••••••••••••'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'password')

        labels = {
            'password': 'Password',
        }

        widgets = {
            'phone': forms.NumberInput(attrs={'class':'form-control my-5', 'placeholder':'09123456789'}),
            'email': forms.EmailInput(attrs={'class':'form-control my-5', 'placeholder':'example1234@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class':'form-control my-5', 'placeholder':'••••••••••••'}),
            'first_name': forms.TextInput(attrs={'class':'form-control my-5', 'placeholder':'John'}),
            'last_name': forms.TextInput(attrs={'class':'form-control my-5', 'placeholder':'Doe'}),
        }

    def clean(self):
        cleaned_data = super(Register, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(message='Passwords are not match!')


class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-5', 'placeholder':'09123456789'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-5', 'placeholder':'••••••••••••'}))
