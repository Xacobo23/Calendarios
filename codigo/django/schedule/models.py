from django.db import models
from datetime import timedelta, datetime
from fp.models import FP
from django.core.exceptions import ValidationError
from enum import Enum
from session.models import Weekday


SCHEDULE_TYPE = [
    ("M", "Mañana"),
    ("T", "Tarde"),
    ("MT", "Mañana y Tarde"),
]

class ScheduleConfig(models.Model):
    # pa facer o final
    name = models.CharField(max_length=200,unique=True)
    schedule_type = models.CharField(max_length=2, choices=SCHEDULE_TYPE)

    start_week_day = models.CharField(max_length=1, choices=Weekday.choices())
    end_week_day = models.CharField(max_length=1, choices=Weekday.choices())

    morning_start_time = models.TimeField(null=True, blank=True)
    morning_end_time = models.TimeField(null=True, blank=True)
    morning_max_sessions = models.IntegerField(default=6)

    afternoon_start_time = models.TimeField(null=True, blank=True)
    afternoon_end_time = models.TimeField(null=True, blank=True)
    afternoon_max_sessions = models.IntegerField(default=6, null=True)

    session_duration = models.DurationField()

    ##metodo para chamar antes de gardar a hora da creación, se lanza a excepcion é que esta mal o dia de inicio e fin
    #deste pau:
    '''
    try:
        schedule.full_clean()  # Validates model fields, including our `clean` method
        schedule.save()
        return redirect("success_page")
    except ValidationError as e:
        return render(request, "schedule_form.html", {"errors": e.message_dict})
    '''
    def clean(self):
        """Ensure that end_week_day is not before start_week_day."""
        weekday_order = {day[0]: index for index, day in enumerate(WEEKDAYS)}  # Map "L" -> 0, "M" -> 1, etc.

        if weekday_order[self.end_week_day] < weekday_order[self.start_week_day]:
            raise ValidationError({"end_week_day": "El día de finalización no puede ser antes del día de inicio."})

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
