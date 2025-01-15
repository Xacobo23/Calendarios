from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.class_list, name='class_list'),  
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]