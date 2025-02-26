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
from classroom.models import Classroom
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
    classrooms = Classroom.objects.all()

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
        'sessionsStructure': sessionsStructure,
        'classrooms': classrooms
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

def my_schedule(request, fp_id, curso=None):
    selected_course = int(curso) if curso else 1

    fp = get_object_or_404(FP, id=fp_id)

    fpScheduleConfig = FPScheduleConfig.objects.filter(fp=fp, fp_course=selected_course).first()
    scheduleConfig = fpScheduleConfig.schedule_config if fpScheduleConfig else None
    modules = Module.objects.filter(fp=fp, course=selected_course) #modulos
    classrooms = Classroom.objects.all()

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
        'sessionsStructure': sessionsStructure,
        'classrooms': classrooms
    }
    return render(request, 'my-schedule.html', data)





