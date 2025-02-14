from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model

from fp.models import FP
from session.models import Weekday
from module.models import Module, Enrolled
from session.models import Session
from .models import ScheduleConfig, FPScheduleConfig, WEEKDAYS
from module.models import Module
from datetime import datetime, timedelta
from collections import defaultdict


from .schedule_functions import generate_schedule_hours


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
    module_ids = modules.values_list('id', flat=True) #array cos ids dos modulos pa filtrar sesions

    scheduleHours = {} #lista de horas
    savedSessions = {} #sesions gardadas na base de datos
    savedSessionsByDay = defaultdict(list) #sesions da bd separadas por día
    sessionsStructure = None
    if scheduleConfig and modules:
        #genero as horas
        scheduleHours = generate_schedule_hours(scheduleConfig)

        #genero as sesions por día
        savedSessions = Session.objects.filter(module__id__in=module_ids).order_by('week_day', 'position')
        for session in savedSessions:
            savedSessionsByDay[session.week_day].append(session)
        savedSessionsByDay=dict(savedSessionsByDay)

        #pillo de que día a que día vai a plantilla
        days = list(Weekday)
        firstDayIndex = Weekday.index_of(scheduleConfig.start_week_day)
        lastDayIndex = Weekday.index_of(scheduleConfig.end_week_day)

        #fago a estructura das sesións, separandoas por día, se en algunha posicion xa hai unha sesión existente, meto os seus datos
        sessionsStructure = defaultdict(lambda: defaultdict(list))
        for day in days[firstDayIndex:lastDayIndex+1]: #creo as sesions pa cada dia
            for dayMoment, hours in scheduleHours.items(): #separadas por mañan e tarde
                sessionsStructure[day.value][dayMoment] = {}
                for sessionPosition in hours.keys():#comprobo se xa hai unha sesión para esa hora e meto os datos
                    sessionsStructure[day.value][dayMoment][sessionPosition] = None
                    #comprobo se xa ten modulo en esa sesión, e se o ten metoo
                    if day.value in savedSessionsByDay:
                        for session in savedSessionsByDay[day.value]:
                            if sessionPosition == session.position:
                                sessionsStructure[day.value][dayMoment][sessionPosition] = session

        # convertir defaultdict a un diccionario normal, porque senon non vai ben na vista
        sessionsStructure = {day: {moment: dict(sessions) for moment, sessions in moments.items()} for day, moments in
                             sessionsStructure.items()}

    data = {
        'title': 'Horario',
        'fp': fp,
        'schedule_config': scheduleConfig,
        'modules': modules,
        'modules_sessions': savedSessions,
        'week_days': WEEKDAYS,
        'scheduleHours': scheduleHours,
        'selected_course': selected_course,
        'savedSessionsByDay': savedSessionsByDay,
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


