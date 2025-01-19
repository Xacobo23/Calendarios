from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

def homepage (request):
    return render(request, 'homepage.html', {'title': 'Inicio'})
