from django.db import models

class Classroom(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f'Clase {self.number}'