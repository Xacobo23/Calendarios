from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),  
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    # path('nombre-vista/', views.ejemplo_vista, name='ejemplo')
]