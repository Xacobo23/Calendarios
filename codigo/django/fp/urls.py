from django.urls import path

from . import views

# Aquí se establecen las rutas a las que va a poder acceder el usuario. El primer parámetro es la ruta en si, el segundo es 
# la vista que se va a cargar (ver archivo views.py) y el tercero es el nombre de esa página en concreto. Este último
# parámetro es importante porque luego se usa para redirigir las páginas con ese nombre.
urlpatterns = [
    path('add/', views.add_fp, name='add_fp'),  
    path('list/', views.fp_list, name='fp_list'),  
    path('edit/<int:fp_id>', views.edit_fp, name='fp_edit'),
    path('delete/<int:fp_id>/', views.delete_fp, name='delete_fp'),
    path('student/list/', views.fp_list_student, name='fp_list_student'),
    path('student/detail/<int:fp_id>', views.fp_detail_student, name='fp_detail_student'),
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]