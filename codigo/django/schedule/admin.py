from django.contrib import admin

from .models import ScheduleConfig, FPScheduleConfig

admin.site.register(ScheduleConfig)
admin.site.register(FPScheduleConfig)

