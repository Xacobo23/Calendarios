from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from fp.models import FP
from fp.forms import FPForm
from module.models import Module, Enrolled
import json

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

def create_tuition (request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    modules = []

    if fp_instance is not None:
        modules = fp_instance.modulos.all()

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Nueva',
        'modules': modules,
        'fp_id': fp_id
    }

    return render(request, 'tuition_create.html', data)

def review_tuition (request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    modules = []

    if fp_instance is not None:
        modules = fp_instance.modulos.all()

    fp_instance = get_object_or_404(FP, id=fp_id)

    form = FPForm(instance=fp_instance)

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Revisar',
        'modules': modules,
        'form': form,
        'fp_id': fp_id
    }

    return render(request, 'tuition_review.html', data)

@csrf_exempt
def make_tuition (request):
    if request.method == 'POST':
        data = json.loads(request.body)
        modules = data.get('modules', [])
        fp_id = data.get('fp_id', None)
        user = request.user

        try:
            for module_id in modules:
                module = Module.objects.get(id=module_id)
                Enrolled.objects.get_or_create(student=user, module=module, course=1)

            return redirect('my_tuitions')
        except Exception as e:
            print(e)

    return redirect('my_tuitions')