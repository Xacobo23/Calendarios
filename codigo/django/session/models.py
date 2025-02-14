from django.db import models
from enum import Enum

from classroom.models import Classroom
from module.models import Module

WEEKDAYS = {
    "L": ["lu", "Lunes"],
    "M": ["ma", "Martes"],
    "X": ["mi", "Miércoles"],
    "J": ["ju", "Jueves"],
    "V": ["vi", "Viernes"],
    "S": ["sa", "Sábado"],
    "D": ["do", "Domingo"],
}

# Enumeración de los días de la semana
class Weekday(Enum):
    LUNES = "L"
    MARTES = "M"
    MIERCOLES = "X"
    JUEVES = "J"
    VIERNES = "V"
    SABADO = "S"
    DOMINGO = "D"

    @classmethod
    def choices(cls):
        return [(day.value, day.name) for day in cls]

    @classmethod
    def human_readable(cls, abbreviation):
        """Returns the full name of the day given its abbreviation."""
        for day in cls:
            if day.value == abbreviation:
                return day.name.capitalize()
        return None  # Return None if abbreviation is not found

    @classmethod
    def index_of(cls, abbreviation):
        """Returns the index of the day based on its abbreviation."""
        days = list(cls)  # Convert enum members to a list
        for index, day in enumerate(days):
            if day.value == abbreviation:
                return index
        return None  # Return None if abbreviation is not found



# Modelo de la tabla Session
class Session(models.Model):
    position = models.PositiveIntegerField()
    week_day = models.CharField(
        max_length=1,
        choices=Weekday.choices()
    )
    class_id = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='sessions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions')
