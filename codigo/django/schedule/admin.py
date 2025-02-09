from django.contrib import admin

from .models import ClassSession, ScheduleConfig

admin.site.register(ClassSession)
admin.site.register(ScheduleConfig)

