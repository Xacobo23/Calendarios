from django.db import models

class Class(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f'Clase {self.number}'