from django.urls import path

from . import views

# Aquí se establecen las rutas a las que va a poder acceder el usuario. El primer parámetro es la ruta en si, el segundo es 
# la vista que se va a cargar (ver archivo views.py) y el tercero es el nombre de esa página en concreto. Este último
# parámetro es importante porque luego se usa para redirigir las páginas con ese nombre.
urlpatterns = [
    path('list/', views.student_list, name='student_list'),  
    path('add/', views.student_add, name='student_add'),
    path('delete/<int:student_id>/', views.student_delete, name='student_delete'),
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]