from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]