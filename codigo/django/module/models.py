from django.db import models
from django.conf import settings

from fp.models import FP


# Se establece el nombre de la tabla(FP) y sus campos. El CharField, TextField... son los tipos de datos que
# se van a almacenar. Dentro de los paréntesis se pueden establecer los atributos que se quiera, por ejemplo
# unique = True, max_legth = 100... Se pueden mirar todos los posibles aquí: https://neunapp.com/contenido/tipos-de-campos-de-un-modelo-en-django-fields-in-models-18329
class Module(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default="#007bff")
    initials = models.CharField(max_length=10)
    credits = models.IntegerField()
    teacher = models.CharField(max_length=100)
    course = models.IntegerField()

    fp = models.ForeignKey(FP, on_delete=models.CASCADE, related_name="modulos")

    def __str__(self):
        return self.name


# Tabla intermedia entre Module y User (Estudiante).
class Enrolled(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    course = models.CharField(max_length=10)

    class Meta:
        unique_together = ("student", "module")

    def __str__(self):
        return self.student.username + " - " + self.module.name + " - " + self.course
