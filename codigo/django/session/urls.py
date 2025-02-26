from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_sessions, name='add_sessions')
]