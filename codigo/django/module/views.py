from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .forms import ModuleForm
from .models import Module
from teacher.models import TeacherModule, Teacher
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


# Esta función solo comprueba si el usuario que quiere acceder es superusuario(admin).
def is_superuser(user):
    return user.is_superuser


# Cada función (def xxxx(request): ) representa una vista. La vista va a tener el nombre de la función.
# El parámetro request es necesario siempre en las vistas, ponérselo y listo.
def module_list(request):
    # Para recuperar los FPs de la base de datos simplemente se llama al modelo FP y con el método .objects.all() se
    # obtienen todas las entradas que tenga la tabla FP. Luego siemplemente se devuelve un renderizado de la request con
    # el nombre del html creado en la carpeta /templates. A mayores se le puede pasar un objeto {} con datos. Por ejemplo
    # se podría pasar un {'title': 'Ejemeplo', 'fps': fps}. Esto haría que en el HTML se pueda llamar a un atributo llamado
    # title y fps y usarlos para pasarles datos o lo que haga falta.
    modules = Module.objects.all()

    total_modules = modules.count()

    data = {
        "title": "Módulos",
        "shortTitle": "Módulo",
        "modules": modules,
        "totalModules": total_modules,
    }

    return render(request, "module_list.html", data)


def module_add(request):
    if request.method == "POST":
        form = ModuleForm(request.POST)

        if form.is_valid():
            module_instance = form.save()

            selected_teachers = form.cleaned_data["teachers"]

            for teacher in selected_teachers:
                TeacherModule.objects.create(
                    teacher=teacher, module=module_instance, cursoEscolar="2024/25"
                )

            messages.success(request, "Nuevo Módulo añadido correctamente.")
            return redirect("module_list")
    else:
        form = ModuleForm()

    data = {
        "title": "Añadir Módulo",
        "form": form,
        "type": "Módulos",
        "module_code": "-",
    }

    return render(request, "module_add.html", data)


def module_edit(request, module_id):
    module_instance = get_object_or_404(Module, id=module_id)
    asociated_modules = []

    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module_instance)

        if form.is_valid():
            form.save()

            selected_teachers = form.cleaned_data["teachers"]
            TeacherModule.objects.filter(module=module_instance).delete()
            for teacher in selected_teachers:
                TeacherModule.objects.create(
                    teacher=teacher, module=module_instance, cursoEscolar="2024/25"
                )

            messages.success(request, "Módulo actualizado correctamente.")
            return redirect("module_list")
        else:
            error_messages = " ".join(
                [
                    f"{field}: {', '.join(errors)}"
                    for field, errors in form.errors.items()
                ]
            )
            messages.error(request, f"Error al editar el Módulo: {error_messages}")
    else:
        form = ModuleForm(instance=module_instance)
        form.fields["teachers"].initial = Teacher.objects.filter(
            teachermodule__module=module_instance
        )

    data = {
        "title": "Editar Módulo",
        "id": module_id,
        "module_code": module_instance.code,
        "shortTitle": "Editar Módulo",
        "form": form,
        "type": "Módulos",
    }

    return render(request, "module_edit.html", data)


@csrf_exempt
def module_delete(request, module_id):
    if request.method == "DELETE":
        module = get_object_or_404(Module, id=module_id)

        module.delete()

        return redirect("module_list")

    return redirect("module_list")
