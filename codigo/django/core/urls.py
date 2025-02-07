from django.urls import path
from django.shortcuts import render
from django.conf.urls import handler404

from . import views

# En esta vista se define la vista cuando no se encuentra una página.
def error_404_view (request, exception):
    data = {
        'title': 'Not Found',
        'error': '404',
        'message': 'Page not found',
    }
    return render(request, '404.html', data=data)

handler404 = error_404_view

urlpatterns = [
    path('', views.homepage, name='homepage'),  
]