from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    
]