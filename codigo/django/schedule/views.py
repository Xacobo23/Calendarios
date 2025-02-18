from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from collections import defaultdict
from django.template.loader import render_to_string

from fp.models import FP
from session.models import Weekday, WEEKDAYS
from module.models import Module, Enrolled
from session.models import Session
from .models import ScheduleConfig, FPScheduleConfig
from module.models import Module
from datetime import datetime, timedelta


from .schedule_functions import generate_schedule_hours
from .schedule_functions import generate_schedule_sessions



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

def view_schedule(request, fp_id, curso=None):
    selected_course = int(curso) if curso else 1

    fp = get_object_or_404(FP, id=fp_id)

    fpScheduleConfig = FPScheduleConfig.objects.filter(fp=fp, fp_course=selected_course).first()
    scheduleConfig = fpScheduleConfig.schedule_config if fpScheduleConfig else None
    modules = Module.objects.filter(fp=fp, course=selected_course) #modulos

    scheduleHours = None #lista de horas
    sessionsStructure = None
    if scheduleConfig and modules:
        #genero as horas
        scheduleHours = generate_schedule_hours(scheduleConfig)

        #genero as sesions por día
        sessionsStructure = generate_schedule_sessions(modules,scheduleConfig,scheduleHours)

    data = {
        'title': 'Horario',
        'fp': fp,
        'schedule_config': scheduleConfig,
        'modules': modules,
        'scheduleHours': scheduleHours,
        'selected_course': selected_course,
        'sessionsStructure': sessionsStructure
    }
    return render(request, 'schedule_view.html', data)

# Vistas alumno
def my_schedules(request):    
    student = request.user
    fps = FP.objects.filter(modulos__enrolled__student=student).distinct()

    data = {
        'title': 'Mis horarios',
        'fps': fps
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





