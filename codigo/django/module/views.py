from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages

from .forms import ModuleForm
from .models import Module


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
        data = request.POST.copy()
        data["color"] = "#112233"  # Valor por defecto
        data["course"] = 1

        form = ModuleForm(data)

        if form.is_valid():
            print("adios")
            form.save()
            messages.success(request, "Nuevo módulo añadido correctamente.")
            return redirect("module_list")
        if not form.is_valid():
            print(
                form.errors
            )  # Esto imprimirá los errores del formulario en la consola

    else:
        form = ModuleForm()

    data = {"title": "Añadir Módulo", "form": form, "type": "Módulo"}

    return render(request, "module_add.html", data)


def module_edit(request, module_id):
    module_code = Module.objects.filter(id=module_id).values_list('code', flat=True).first()

    data = {
        "title": "Editar Módulo",
        "module_code": module_code,
        "type": "Módulo",
        "form": ModuleForm(instance=Module.objects.get(id=module_id)),
    }

    return render(request, "module_edit.html", data)
