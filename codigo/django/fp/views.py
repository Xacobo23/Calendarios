from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import FP
from .forms import FPForm


# Esta función solo comprueba si el usuario que quiere acceder es superusuario(admin).
def is_superuser(user):
    return user.is_superuser


# Cada función (def xxxx(request): ) representa una vista. La vista va a tener el nombre de la función.
# El parámetro request es necesario siempre en las vistas, ponérselo y listo.
def fp_list(request):
    # Para recuperar los FPs de la base de datos simplemente se llama al modelo FP y con el método .objects.all() se
    # obtienen todas las entradas que tenga la tabla FP. Luego siemplemente se devuelve un renderizado de la request con
    # el nombre del html creado en la carpeta /templates. A mayores se le puede pasar un objeto {} con datos. Por ejemplo
    # se podría pasar un {'title': 'Ejemeplo', 'fps': fps}. Esto haría que en el HTML se pueda llamar a un atributo llamado
    # title y fps y usarlos para pasarles datos o lo que haga falta.
    fps = FP.objects.all()

    fields = [field.verbose_name for field in FP._meta.fields]

    fps_data = [
        {field.name: getattr(fp, field.name) for field in FP._meta.fields} for fp in fps
    ]

    totalFp = fps.count()

    data = {
        "title": "Ciclos formativos",
        "shortTitle": "FP",
        "fps_data": fps_data,
        "fields": fields,
        "totalFp": totalFp,
    }

    return render(request, "fp_list.html", data)

def fp_list_student(request):
    # Para recuperar los FPs de la base de datos simplemente se llama al modelo FP y con el método .objects.all() se
    # obtienen todas las entradas que tenga la tabla FP. Luego siemplemente se devuelve un renderizado de la request con
    # el nombre del html creado en la carpeta /templates. A mayores se le puede pasar un objeto {} con datos. Por ejemplo
    # se podría pasar un {'title': 'Ejemeplo', 'fps': fps}. Esto haría que en el HTML se pueda llamar a un atributo llamado
    # title y fps y usarlos para pasarles datos o lo que haga falta.
    fps = FP.objects.all()

    fields = [field.verbose_name for field in FP._meta.fields]

    fps_data = [
        {field.name: getattr(fp, field.name) for field in FP._meta.fields} for fp in fps
    ]

    totalFp = fps.count()

    data = {
        "title": "Ciclos formativos",
        "shortTitle": "FP",
        "fps_data": fps_data,
        "fields": fields,
        "totalFp": totalFp,
    }

    return render(request, "fp_list_student.html", data)


# @user_passes_test(is_superuser)
def add_fp(request):
    if request.method == "POST":
        form = FPForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo FP añadido correctamente.")
            return redirect("fp_list")
    else:
        form = FPForm()

    data = {
        "title": "Añadir FP",
        "form": form,
        "type": "Ciclos Formativos",
        'fp_code': '-'
        }

    return render(request, "fp_add.html", data)


def edit_fp(request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    asociated_modules = []

    if fp_instance is not None:
        asociated_modules = fp_instance.modulos.all()

    if request.method == 'POST':
        form = FPForm(request.POST, instance=fp_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'FP actualizado correctamente.')
            return redirect('fp_list')
        else:
            error_messages = " ".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
            messages.error(request, f"Error al editar el FP: {error_messages}")
    else:
        form = FPForm(instance=fp_instance)

    data = {
        "title": "Editar FP",
        "id": fp_id,
        "fp_code": fp_instance.code,
        "shortTitle": "Editar FP",
        "form": form,
        "type": "Ciclos Formativos",
        "asociated_modules": asociated_modules
    }

    return render(request, "fp_edit.html", data)

@csrf_exempt
def delete_fp(request, fp_id):
    if request.method == 'DELETE':
        fp = get_object_or_404(FP, id=fp_id)

        fp.delete()

        return redirect('fp_list')
    
    return redirect('fp_list')

def fp_detail_student (request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    modules = []

    if fp_instance is not None:
        modules = fp_instance.modulos.all()

    fp_instance = get_object_or_404(FP, id=fp_id)

    form = FPForm(instance=fp_instance)

    data = {
        'title': 'Ciclos Formativos',
        'subTitle': fp_instance.initials,
        'modules': modules,
        'form': form,
        'fp_id': fp_id
    }

    return render(request, 'fp_see_details.html', data)



