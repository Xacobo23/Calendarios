from django.db import models
from datetime import timedelta, datetime
from fp.models import FP

WEEKDAYS = [
    ("L", "Lunes"),
    ("M", "Martes"),
    ("X", "Miércoles"),
    ("J", "Jueves"),
    ("V", "Viernes"),
    ("S", "Sábado"),
    ("D", "Domingo"),
]

SCHEDULE_TYPE = [
    ("M", "Mañana"),
    ("T", "Tarde"),
    ("MT", "Mañana y Tarde"),
]

class ScheduleConfig(models.Model):
    schedule_type = models.CharField(max_length=2, choices=SCHEDULE_TYPE)

    start_week_day = models.IntegerField()
    end_week_day = models.IntegerField()

    morning_start_time = models.TimeField(null=True, blank=True)
    morning_end_time = models.TimeField(null=True, blank=True)
    morning_max_sessions = models.IntegerField(default=6)

    afternoon_start_time = models.TimeField(null=True, blank=True)
    afternoon_end_time = models.TimeField(null=True, blank=True)
    afternoon_max_sessions = models.IntegerField(default=6)

    session_duration = models.DurationField()

    def save(self, *args, **kwargs):
        if self.session_duration:
            if self.morning_start_time and self.morning_max_sessions:
                self.morning_end_time = (
                    datetime.combine(datetime.today(), self.morning_start_time)
                    + self.session_duration * self.morning_max_sessions
                ).time()

            if self.afternoon_start_time and self.afternoon_max_sessions:
                self.afternoon_end_time = (
                    datetime.combine(datetime.today(), self.afternoon_start_time)
                    + self.session_duration * self.afternoon_max_sessions
                ).time()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_schedule_type_display()} ({self.start_week_day}-{self.end_week_day})"
    
class FPScheduleConfig(models.Model):
    fp = models.ForeignKey(FP, on_delete=models.CASCADE)
    schedule_config = models.ForeignKey(ScheduleConfig, on_delete=models.CASCADE)
    fp_course = models.IntegerField()

    class Meta:
        unique_together = ["fp", "schedule_config", "fp_course"]

    def __str__(self):
        return f"{self.fp} - {self.schedule_config} ({self.fp_course})"
