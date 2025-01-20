from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

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