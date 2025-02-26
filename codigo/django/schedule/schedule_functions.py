#generate_schedule_hours
from datetime import datetime

# generate_schedule_sessions
from collections import defaultdict
from session.models import Session
from session.models import Weekday, WEEKDAYS

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
    module_ids = modules.values_list('id', flat=True) #array cos ids dos modulos pa filtrar sesions
    savedSessionsByDay = defaultdict(list) #sesions da bd separadas por día

    # genero as sesions por día
    savedSessions = Session.objects.filter(module__id__in=module_ids).order_by('week_day', 'position')
    for session in savedSessions:
        savedSessionsByDay[session.week_day].append(session)
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