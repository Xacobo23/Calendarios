from django.urls import path

from . import views

urlpatterns = [
    path('view-schedule/', views.view_schedule, name='view_schedule'),  
]