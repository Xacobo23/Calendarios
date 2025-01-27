from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def view_schedule(request):
    data = {
        'title': 'Horario',
        
    }
    return render(request, 'schedule_view.html', data)