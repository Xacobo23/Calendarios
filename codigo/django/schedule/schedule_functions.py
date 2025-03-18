#generate_schedule_hours
from datetime import datetime

# generate_schedule_sessions
from collections import defaultdict
from session.models import Session
from session.models import Weekday, WEEKDAYS

import random


#genera
def generate_schedule_hours(scheduleConfig):
    scheduleHours = {}
    i = 1  # Posición de la sesión

    # Generar todas las horas de sesiones
    if scheduleConfig.schedule_type in ("M", "MT"):
        scheduleHours["Mañana"] = {}
        current_time = datetime.combine(datetime.today(), scheduleConfig.morning_start_time)
        for i in range(i, scheduleConfig.morning_max_sessions + 1):
            scheduleHours["Mañana"][i] = {
                "start": current_time.time().strftime('%H:%M')
            }
            current_time += scheduleConfig.session_duration
            scheduleHours["Mañana"][i]["end"] = current_time.time().strftime('%H:%M')

    if scheduleConfig.schedule_type in ("T", "MT"):
        scheduleHours["Tarde"] = {}
        totalSessionsNumber = scheduleConfig.afternoon_max_sessions
        if scheduleConfig.schedule_type == "MT":  # Ajustar si hay sesiones de mañana
            totalSessionsNumber += scheduleConfig.morning_max_sessions

        current_time = datetime.combine(datetime.today(), scheduleConfig.afternoon_start_time)
        for i in range(i, totalSessionsNumber):
            scheduleHours["Tarde"][i] = {
                "start": current_time.time().strftime('%H:%M')
            }
            current_time += scheduleConfig.session_duration
            scheduleHours["Tarde"][i]["end"] = current_time.time().strftime('%H:%M')

    return scheduleHours


#generar as sesións de cada día
def generate_schedule_sessions(modules, scheduleConfig, scheduleHours):
    #camio de colores dos modulos das sesions
    # colores disponibles
    pastel_colors = [
        "#FAD9D6", "#FFE2E2", "#FFD6E0", "#FDE2E4", "#FFDFD3",
        "#FCE8CB", "#F8ECD5", "#F5F7DC", "#E9F7EF", "#D8F3DC",
        "#B7E4C7", "#A0C4FF", "#CAE4DB", "#BEE9E8", "#B9FBC0",
        "#C2E9FB", "#E3F2FD", "#CFE2F3", "#EADFFD",
        "#D4BEEB", "#DAC7FF", "#F3D5F4", "#F9CFEF", "#E8D3F9",
        "#FFE4E1", "#FFEEDD", "#FFF9E6", "#E3EDCD", "#C4F1F9",
        "#E3FFF4", "#DAE5D6", "#D8E1D4", "#D9F4FF", "#C6E9FF",
        "#F2F7FF", "#FCE4EC", "#F9E4D7", "#F6E8EA", "#FBE7C6"
    ]
    #modulos aos que lles cambiei o color
    changed_module_ids = {}

    module_ids = modules.values_list('id', flat=True) #array cos ids dos modulos pa filtrar sesions
    savedSessionsByDay = defaultdict(list) #sesions da bd separadas por día

    # genero as sesions por día
    savedSessions = Session.objects.filter(module__id__in=module_ids).order_by('week_day', 'position')
    for session in savedSessions:
        savedSessionsByDay[session.week_day].append(session)

        #cambio o color do modulo pa que se ciña a paleta
        if session.module:
            if session.module.id not in changed_module_ids:
                color = pastel_colors.pop(random.randrange(len(pastel_colors)))
                changed_module_ids[session.module.id] = color
            else:
                color = changed_module_ids[session.module.id]
            session.module.color = color


    savedSessionsByDay = dict(savedSessionsByDay)

    # pillo de que día a que día vai a plantilla
    days = list(Weekday)
    firstDayIndex = Weekday.index_of(scheduleConfig.start_week_day)
    lastDayIndex = Weekday.index_of(scheduleConfig.end_week_day)

    # Estructura de sesiones con información extra sobre el día
    sessionsStructure = defaultdict(lambda: {"shortName": "", "fullName": "", "sessions": defaultdict(dict)})

    for day in days[firstDayIndex:lastDayIndex + 1]:  # Para cada día en el rango
        sessionsStructure[day.value]["shortName"] = WEEKDAYS[day.value][0]  # "lu"
        sessionsStructure[day.value]["fullName"] = WEEKDAYS[day.value][1]  # "Lunes"

        for dayMoment, hours in scheduleHours.items():  # Mañana/Tarde
            sessionsStructure[day.value]["sessions"][dayMoment] = {}

            for sessionPosition in hours.keys():
                sessionsStructure[day.value]["sessions"][dayMoment][sessionPosition] = None

                # Si ya existe una sesión guardada en este día y posición, la insertamos
                if day.value in savedSessionsByDay:
                    for session in savedSessionsByDay[day.value]:
                        if sessionPosition == session.position:
                            sessionsStructure[day.value]["sessions"][dayMoment][sessionPosition] = session

    # Convertir defaultdict en un diccionario normal
    sessionsStructure = {
        day: {
            "shortName": data["shortName"],
            "fullName": data["fullName"],
            "sessions": {moment: dict(sessions) for moment, sessions in data["sessions"].items()}
        }
        for day, data in sessionsStructure.items()
    }

    return sessionsStructure