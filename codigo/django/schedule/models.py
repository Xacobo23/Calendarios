from django.db import models
from module.models import Module

WEEKDAYS = [
        ("L", "Lunes"),
        ("M", "Martes"),
        ("X", "Miércoles"),
        ("J", "Jueves"),
        ("V", "Viernes"),
        ("S", "Sábado"),
        ("D", "Domingo"),
    ]

class ClassSession(models.Model):
    # Clave externa que relaciona la sesión con un módulo
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="class_sessions"
    )

    # Día de la semana (ej: "Lunes", "Martes", etc.)
    
    weekday = models.CharField(max_length=1, choices=WEEKDAYS)  # Día de la semana

    # Sesiones predefinidas
    SESSIONS = [
        # Clase pola mañán
        ("S1", "Session 1 (08:45-09:35)"),
        ("S2", "Session 2 (09:35-10:25)"),
        ("S3", "Session 3 (10:25-11:15)"),
        ("S4", "Session 4 (11:15-12:05)"),
        ("S5", "Session 5 (12:05-12:55)"),
        ("S6", "Session 6 (12:55-13:45)"),
        ("S7", "Session 7 (13:45-14:35)"),
        # Clase pola tarde ordinaria
        ("S8", "Session 8 (16:00-16:50)"),
        ("S9", "Session 9 (16:50-17:40)"),
        # Clases pola tarde
        ("S10", "Session 10 (17:40-18:30)"),
        ("S11", "Session 11 (18:30-19:20)"),
        ("S12", "Session 12 (19:20-20:10)"),
        ("S13", "Session 13 (20:10-21:00)"),
        ("S14", "Session 14 (21:00-21:50)"),
        ("S15", "Session 15 (21:50-22:40)"),
        ("S16", "Session 16 (22:40-23:30)"),
    ]
    session = models.CharField(max_length=3, choices=SESSIONS)  # Sesión predefinida

    # Número de clase (ej: 1, 2, 3...)
    class_number = models.IntegerField()

    def __str__(self):
        return f"{self.module.name} - {self.get_weekday_display()} {self.get_session_display()} (Clase {self.class_number})"

    class Meta:
        # Evita duplicados en la combinación de módulo, día y número de clase
        unique_together = ("module", "session", "class_number")

class ScheduleConfig (models.Model):
    morning_start_time = models.TimeField()
    morning_end_time = models.TimeField()

    afternoon_start_time = models.TimeField()
    afternoon_end_time = models.TimeField()

    session_duration = models.DurationField()
