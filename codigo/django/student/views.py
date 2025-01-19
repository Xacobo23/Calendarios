from django.shortcuts import render
from django.contrib.auth import get_user_model  

User = get_user_model()

def student_list (request): 
    students = User.objects.values('id', 'dni', 'phone', 'username', 'email', 'first_name', 'last_name')

    total_students = students.count()

    data = {
        'title': 'Estudiantes',
        'shortTitle': 'Estudiante',
        'students': students,
        'totalStudents': total_students
    }
    return render(request, 'student_list.html', data)
