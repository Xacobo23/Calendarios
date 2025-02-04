from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .models import Teacher
from .forms import TeacherForm

def is_superuser(user):
    return user.is_superuser

def teacher_list(request):

    teachers = Teacher.objects.all()

    total_teachers = teachers.count()

    data = {
        "title": "Profesores/a",
        "shortTitle": "Profesor",
        "teachers": teachers,
        "totalTeachers": total_teachers,
    }

    return render(request, "teacher_list.html", data)

def teacher_add(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            teacher_instance = form.save()

            messages.success(request, "Nuevo Profesor añadido correctamente.")
            return redirect("teacher_list")
    else:
        form = TeacherForm()

    data = {
        "title": "Añadir Profesor",
        "form": form,
        "type": "Profesores",
        'teacher_code': '-'
        }

    return render(request, "teacher_add.html", data)

def teacher_edit(request, teacher_id):
    teacher_instance = get_object_or_404(Teacher, id=teacher_id)
    asociated_modules = []

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor actualizado correctamente.')
            return redirect('teacher_list')
        else:
            error_messages = " ".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
            messages.error(request, f"Error al editar el Módulo: {error_messages}")
    else:
        form = TeacherForm(instance=teacher_instance)

    data = {
        "title": "Editar Profesor",
        "id": teacher_id,
        "shortTitle": "Editar Profesor",
        "form": form,
        "teacher_email": teacher_instance.email,
        "id": teacher_instance.id,
        "type": "Profesor",
    }

    return render(request, "teacher_edit.html", data)

@csrf_exempt
def delete_teacher(request, teacher_id):
    if request.method == 'DELETE':
        teacher = get_object_or_404(Teacher, id=teacher_id)

        teacher.delete()

        return redirect('teacher_list')
    
    return redirect('teacher_list')
