from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.class_list, name='class_list'),  
]