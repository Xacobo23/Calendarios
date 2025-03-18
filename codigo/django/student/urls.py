from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.student_list, name="student_list"),
    path("add/", views.student_add, name="student_add"),
    path("import/", views.student_import, name="student_import"),
    path("edit/<int:student_id>/", views.student_edit, name="student_edit"),
    path("delete/<int:student_id>/", views.delete_student, name="student_delete"),
    path('restore-password/<int:student_id>', views.restore_password, name='restore_password'),
    path('edit-fp/<int:student_id>/<int:fp_id>', views.student_fp_edit, name='student_fp_edit')
]
