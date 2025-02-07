from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from fp.models import FP
from module.models import Module, Enrolled
from session.models import Session

def select_schedule(request):
    fps = FP.objects.all()

    total_fp = fps.count()

    data = {
        'title': 'Horarios',
        'fps': fps,
        'shortTitle': 'Horario',
        'totalFp': total_fp
    }

    return render(request, 'schedule_select.html', data)

def view_schedule(request, fp_id):
    fp = get_object_or_404(FP, id=fp_id)

    data = {
        'title': 'Horario',
        'fp': fp,
    }

    return render(request, 'schedule_view.html', data)

def my_schedules(request):
    data = {
        'title': 'Mis horarios',
    }

    return render(request, 'my-schedules.html', data)

def my_schedule(request, fp_id):
    fp = get_object_or_404(FP, id=fp_id)

    # Filtrar los módulos en los que está matriculado el usuario dentro del FP específico
    enrolled_modules = Module.objects.filter(
        id__in=Enrolled.objects.filter(student=request.user).values_list('module_id', flat=True),
        fp=fp
    )

    module_sessions = {}

    for module in enrolled_modules:
        sessions = module.sessions.all()
        module_sessions[module] = sessions

    for module, sessions in module_sessions.items():
        for session in sessions:
            print(module, session.start_time, session.end_time, session.week_day)

    week_days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']

    data = {
        'title': 'Mi horario',  
        'fp': fp,
        'enrolled_modules': enrolled_modules, 
        'module_sessions': module_sessions,
        'week_days': week_days,
    }

    return render(request, 'my-schedule.html', data)


