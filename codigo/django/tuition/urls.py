from django.urls import path

from . import views

urlpatterns = [
    path("my-tuitions/", views.my_tuitions, name="my_tuitions"),
    path('select-tuition/', views.select_tuition, name='select_tuition'),
    path('create-tuition/<int:fp_id>/', views.create_tuition, name='create_tuition'),
]
