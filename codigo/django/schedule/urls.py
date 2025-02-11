from django.urls import path

from . import views

urlpatterns = [
    path('select-schedule/', views.select_schedule, name='select_schedule'),
    path('view-schedule/<int:fp_id>/<int:curso>', views.view_schedule, name='view_schedule'),
    path('my-schedules/', views.my_schedules, name='my_schedules'),
    path('my-schedule/<int:fp_id>', views.my_schedule, name='my_schedule'),
]