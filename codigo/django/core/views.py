from django.shortcuts import redirect

# Vista principal al abrir la página (todo redirecciones).
def homepage (request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('student_list')
        else:
            return redirect('my_schedules')
    else:
        return redirect('login')

