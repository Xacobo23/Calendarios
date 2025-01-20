from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from student.models import CustomUser

class RegisterForm (UserCreationForm):
    email = forms.EmailField()
    dni = forms.CharField(max_length=15, required=True)
    phone = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def clean_phone (self):
        phone = self.cleaned_data('phone')
        return phone