from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from student.forms import CustomUserChangeForm

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
        form = UsuarioForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create(
                dni=data["dni"],
                first_name=data["first_name"],
                last_name=data["apel1"]
                + " "
                + (data["apel2"] if data["apel2"] else ""),
                email=data["email"],
                username=data["loginEmail"],
                phone=data["phone"],
            )
            user.save()

            messages.success(request, "Estudiante añadido correctamente.")
            return redirect("student_add")
        else:
            messages.error(request, "Error al añadir el estudiante.")
    else:
        form = UsuarioForm()

    data = {"title": "Añadir Estudiante", "form": form, "type": "Alumnos"}
    return render(request, "student_add.html", data)


def student_edit(request, student_id):
    student = get_object_or_404(get_user_model(), id=student_id)

    dni = student.dni

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=student)  # Asociar el form con el usuario
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Estudiante actualizado correctamente.')
            return redirect("student_list")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo {field.label}: {error}")
            messages.error(request, "Error al actualizar el estudiante.")
    else:
        # Usar instance=student para evitar errores en la inicialización
        form = CustomUserChangeForm(
            instance=student,
            initial={
                "apel1": student.last_name.split()[0] if student.last_name else "",
                "apel2": student.last_name.split()[1] if len(student.last_name.split()) > 1 else "",
                "loginEmail": student.username,
            },
        )

    data = {
        "title": "Editar Estudiante",
        "type": "Alumnos",
        "form": form,
        "student_id": student_id,
        'dni': dni
    }
    return render(request, "student_edit.html", data)

def student_delete(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(User, id=student_id)
        student.delete()
        messages.success(request, "Estudiante eliminado correctamente.")
        return redirect("student_list")

    return redirect("student_list")
