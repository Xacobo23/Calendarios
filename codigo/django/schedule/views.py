from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model

from fp.models import FP
from module.models import Module, Enrolled
from session.models import Session
from .models import ScheduleConfig, FPScheduleConfig, WEEKDAYS
from module.models import Module
from datetime import datetime, timedelta


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

    fpScheduleConfig = FPScheduleConfig.objects.filter(fp=fp, fp_course=curso).first()
    scheduleConfig = fpScheduleConfig.schedule_config if fpScheduleConfig else None

    scheduleHours = {}
    if scheduleConfig:
        i = 1 #posicion de la sesion

        #genero todas as horas de sesions
        if scheduleConfig.schedule_type == "M" or scheduleConfig.schedule_type == "MT":
            scheduleHours["Mañana"]={}

            current_time = datetime.combine(datetime.today(), scheduleConfig.morning_start_time)
            for i in range(i,scheduleConfig.morning_max_sessions):
                scheduleHours["Mañana"][i]={}
                start = current_time
                scheduleHours["Mañana"][i]["start"]=start.time().strftime('%H:%M')
                current_time+=scheduleConfig.session_duration
                end = current_time
                scheduleHours["Mañana"][i]["end"]=end.time().strftime('%H:%M')
        if scheduleConfig.schedule_type == "T" or scheduleConfig.schedule_type == "MT":
            scheduleHours["Tarde"] = {}
            totalSessionsNumber = scheduleConfig.afternoon_max_sessions
            if scheduleConfig.schedule_type == "MT": #se tamen ten sesions de mañan hai que sumalas para que vaia correctamente
                totalSessionsNumber = scheduleConfig.afternoon_max_sessions + scheduleConfig.morning_max_sessions

            current_time = datetime.combine(datetime.today(), scheduleConfig.afternoon_start_time)
            for i in range(i, totalSessionsNumber):
                scheduleHours["Tarde"][i] = {}
                start = current_time
                scheduleHours["Tarde"][i]["start"] = start.time().strftime('%H:%M')
                current_time += scheduleConfig.session_duration
                end = current_time
                scheduleHours["Tarde"][i]["end"] = end.time().strftime('%H:%M')
        print(scheduleHours)

        print(scheduleConfig.schedule_type)




    modules = Module.objects.filter(fp=fp, course=curso)

    modules_sessions = {}

    for module in modules:
        sessions = Session.objects.filter(module=module)
        modules_sessions[module] = sessions

    print(modules_sessions)
    
    data = {
        'title': 'Horario',
        'fp': fp,
        'schedule_config': scheduleConfig,
        'modules': modules,
        'modules_sessions': modules_sessions,
        'week_days': WEEKDAYS,
        'scheduleHours': scheduleHours,
        'selected_course': selected_course
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


