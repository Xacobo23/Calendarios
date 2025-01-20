from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=15, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=False, blank=False)

    def __str__(self):
        return self.username
