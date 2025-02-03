from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from fp.models import FP

def select_schedule (request):

    fps = FP.objects.all()

    data = {
        'title': 'Horarios',
        'fps': fps,
    }

    return render(request, 'schedule_select.html', data)

def view_schedule(request, fp_id):
    
    fp = FP.objects.get(id=fp_id)

    data = {
        'title': 'Horario',
        'fp': fp,
    }

    return render(request, 'schedule_view.html', data)