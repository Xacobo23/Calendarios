from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.teacher_list, name="teacher_list"),
    path("edit/<int:teacher_id>", views.teacher_edit, name='teacher_edit')
]
