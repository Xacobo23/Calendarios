from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from user.forms import CustomUserCreationForm

User = get_user_model()


# Vista de Administrador para listar los estudiantes.
def student_list(request):
    # Obtiene los usuarios que no son superusuarios.
    students = User.objects.filter(is_superuser=False).values(
        "id", "dni", "phone", "username", "email", "first_name", "last_name"
    )

    total_students = students.count()

    data = {
        "title": "Alumnos",
        "shortTitle": "Estudiante",
        "students": students,
        "totalStudents": total_students,
    }

    return render(request, "student_list.html", data)


def student_add(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante añadido correctamente.")
            return redirect("student_add")
        else:
            messages.error(request, "Error al añadir el estudiante.")
    else:
        form = CustomUserCreationForm()

    data = {"title": "Añadir Estudiante", "form": form, "type": "Alumnos"}

    return render(request, "student_add.html", data)


def student_edit(request, student_id):
    student_dni = User.objects.filter(id=student_id).values_list('dni', flat=True).first()

    data = {
        "title": "Añadir Estudiante",
        "type": "Alumnos",
        "dni": student_dni,
        "form": CustomUserCreationForm(),
    }
    return render(request, "student_edit.html", data)


def student_delete(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(User, id=student_id)
        student.delete()
        messages.success(request, "Estudiante eliminado correctamente.")
        return redirect("student_list")

    return redirect("student_list")
