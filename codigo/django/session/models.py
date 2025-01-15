from django.db import models
from enum import Enum

from classroom.models import Classroom
from module.models import Module

# Enumeración de los días de la semana
class Weekday(Enum):
    MONDAY = 'lunes'
    TUESDAY = 'martes'
    WEDNESDAY = 'miercoles'
    THURSDAY = 'jueves'
    FRIDAY = 'viernes'

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]

# Modelo de la tabla Session
class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    week_day = models.CharField(
        max_length=10, 
        choices=Weekday.choices()
    )
    class_id = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='sessions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions')
