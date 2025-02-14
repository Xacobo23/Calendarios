from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm


from .forms import CustomUserCreationForm

# Create your views here.

def register (request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro completado con éxito! Iniciando sesión...')
            return redirect('homepage')
        else:
            messages.error(request, 'Error en el registro. Verifica los datos.')
    else:
        form = CustomUserCreationForm()

    return render (request, 'registration/register.html', {'form': form})

class CustomLoginView (LoginView):
    template_name = 'registration/login.html'

    def form_valid (self, form):
        response = super().form_valid(form)

        if self.request.user.restart_password:
            self.request.user.restart_password = False
            self.request.user.save()
            return redirect('change_password')

        messages.success(self.request, f'Bienvenido/a {self.request.user.first_name}!')

        return response
    
    def form_invalid (self, form):
        response = super().form_invalid(form)

        messages.error(self.request, 'Error en el inicio de sesión. Verifica los datos.')

        return response
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña actualizada con éxito!')
            return redirect('homepage')
        else:
            messages.error(request, 'Error al actualizar la contraseña. Verifica los datos.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/change_password.html', {'form': form})