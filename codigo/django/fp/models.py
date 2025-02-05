from django.db import models
from enum import Enum


# Enum para representar el tipo de FP (Básico, Medio o Superior).
# Se establecen los valores que se van a usar(en mayúscula) y se le relaciona el valor que va a escribir en la BD.
class FPType(Enum):
    BASICO = "basico"
    MEDIO = "medio"
    SUPERIOR = "superior"
    CURSO_ESPECIALIZACION = "especializacion"

    @classmethod
    def choices(cls):
        return [(item.name, item.value.upper()) for item in cls]


# Se establece el nombre de la tabla(FP) y sus campos. El CharField, TextField... son los tipos de datos que
# se van a almacenar. Dentro de los paréntesis se pueden establecer los atributos que se quiera, por ejemplo
# unique = True, max_legth = 100... Se pueden mirar todos los posibles aquí: https://neunapp.com/contenido/tipos-de-campos-de-un-modelo-en-django-fields-in-models-18329
class FP(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024)
    fp_type = models.CharField(
        max_length=40, choices=FPType.choices(), default=FPType.MEDIO.name
    )
    short_name = models.CharField(max_length=100)
    duration = models.IntegerField()
    initials = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.get_fp_type_display()})"
