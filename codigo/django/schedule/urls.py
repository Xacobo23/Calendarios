from django.urls import path

from . import views

urlpatterns = [
    path('select-schedule/', views.select_schedule, name='select_schedule'),
    path('view-schedule/<int:fp_id>', views.view_schedule, name='view_schedule'),  
]