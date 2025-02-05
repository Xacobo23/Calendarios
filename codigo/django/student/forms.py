from django import forms


class UsuarioForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=10)
    first_name = forms.CharField(label="Nombre", max_length=100)
    apel1 = forms.CharField(label="Primer Apellido", max_length=100)
    apel2 = forms.CharField(label="Segundo Apellido", max_length=100, required=False)
    email = forms.EmailField(label="Correo electrónico")
    phone = forms.CharField(label="Teléfono", max_length=15)
    loginEmail = forms.CharField(label="Email de login", max_length=150)
    force_password_change = forms.BooleanField(
        label="Forzar cambio de contraseña en el siguiente login:", required=False
    )
