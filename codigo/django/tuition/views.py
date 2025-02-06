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