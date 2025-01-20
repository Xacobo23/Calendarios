from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class CustomUserCreationForm (UserCreationForm):
    dni = forms.CharField(max_length=15, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
