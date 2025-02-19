from django.urls import path

from . import views

# Aquí se establecen las rutas a las que va a poder acceder el usuario. El primer parámetro es la ruta en si, el segundo es
# la vista que se va a cargar (ver archivo views.py) y el tercero es el nombre de esa página en concreto. Este último
# parámetro es importante porque luego se usa para redirigir las páginas con ese nombre.
urlpatterns = [
    # path('add/', views.add_module, name='add_module'),
    path("list/", views.module_list, name="module_list"),
    path("add/", views.module_add, name="module_add"),
    path("edit/<int:module_id>", views.module_edit, name="module_edit"),
    path("delete/<int:module_id>/", views.module_delete, name="module_delete"),
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]
