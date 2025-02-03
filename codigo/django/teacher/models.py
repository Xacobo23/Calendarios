from django.db import models
from module.models import Module


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    modules = models.ManyToManyField(
        Module, through="TeacherModule", related_name="teachers"
    )

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.dni}"


# Tabla intermedia TeacherModule
class TeacherModule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    cursoEscolar = models.CharField(max_length=10)  # ie: "2024/25"

    class Meta:
        unique_together = ("teacher", "module", "cursoEscolar")
