from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

# Aquí se establecen las rutas a las que va a poder acceder el usuario. El primer parámetro es la ruta en si, el segundo es 
# la vista que se va a cargar (ver archivo views.py) y el tercero es el nombre de esa página en concreto. Este último
# parámetro es importante porque luego se usa para redirigir las páginas con ese nombre.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]