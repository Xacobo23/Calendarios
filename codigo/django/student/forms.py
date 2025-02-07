from django import forms
from django.contrib.auth import get_user_model

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'dni', 'phone', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'form-control',
                'id': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Correo electrónico',
                'class': 'form-control',
                'id': 'email'
            }),
            'dni': forms.TextInput(attrs={
                'placeholder': 'Documento Nacional de Identidad',
                'class': 'form-control',
                'id': 'dni'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Número de teléfono',
                'class': 'form-control',
                'id': 'phone'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Primer nombre',
                'class': 'form-control',
                'id': 'first_name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Apellido',
                'class': 'form-control',
                'id': 'last_name'
            }),
        }

    # Opcional: Definir labels personalizados si quieres personalizar los textos de las etiquetas
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    dni = forms.CharField(label='DNI')
    phone = forms.CharField(label='Teléfono')
    first_name = forms.CharField(label='Primer nombre')
    last_name = forms.CharField(label='Apellido')

# class UsuarioForm(forms.Form):
#     dni = forms.CharField(label="DNI", max_length=10)
#     first_name = forms.CharField(label="Nombre", max_length=100)
#     apel1 = forms.CharField(label="Primer Apellido", max_length=100)
#     apel2 = forms.CharField(label="Segundo Apellido", max_length=100, required=False)
#     email = forms.EmailField(label="Correo electrónico")
#     phone = forms.CharField(label="Teléfono", max_length=15)
#     loginEmail = forms.CharField(label="Email de login", max_length=150)
#     force_password_change = forms.BooleanField(
#         label="Forzar cambio de contraseña en el siguiente login:", required=False
#     )
