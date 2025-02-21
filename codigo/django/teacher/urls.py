from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.teacher_list, name="teacher_list"),
    path("add/", views.teacher_add, name="teacher_add"),
    path("edit/<int:teacher_id>", views.teacher_edit, name="teacher_edit"),
    path("delete/<int:teacher_id>/", views.delete_teacher, name="teacher_delete"),
]
