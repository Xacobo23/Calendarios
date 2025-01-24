from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model  
from django.contrib import messages

from user.forms import CustomUserCreationForm

User = get_user_model()

# Vista de Administrador para listar los estudiantes.
def student_list (request): 
    # Obtiene los usuarios que no son superusuarios.
    students = User.objects.filter(is_superuser=False).values('id', 'dni', 'phone', 'username', 'email', 'first_name', 'last_name')

    total_students = students.count()

    data = {
        'title': 'Estudiantes',
        'shortTitle': 'Estudiante',
        'students': students,
        'totalStudents': total_students
    }

    return render(request, 'student_list.html', data)

def student_add (request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante añadido correctamente.')
            return redirect('student_add')
        else:
            messages.error(request, 'Error al añadir el estudiante.')
    else:
        form = CustomUserCreationForm()

    data = {
        'title': 'Añadir Estudiante',
        'form': form
    }

    return render(request, 'student_add.html', data)
