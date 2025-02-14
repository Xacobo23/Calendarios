from datetime import datetime


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