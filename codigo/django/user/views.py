from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

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

        messages.success(self.request, f'Bienvenido/a {self.request.user.first_name}!')

        return response
    
    def form_invalid (self, form):
        response = super().form_invalid(form)

        messages.error(self.request, 'Error en el inicio de sesión. Verifica los datos.')

        return response