from django.shortcuts import render

from fp.models import FP

def my_tuitions (request):
    user = request.user

    fps = FP.objects.filter(modulos__enrolled__student=user).distinct().prefetch_related('modulos')

    data = {
        'title': 'Mis matrículas',
        'fps': fps
    }

    return render(request, 'my_tuitions.html', data)

def select_tuition (request):
    fps = FP.objects.all()

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Nueva',
        'fps': fps
    }

    return render(request, 'tuition_select.html', data)