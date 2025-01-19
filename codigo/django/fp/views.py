from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from .models import FP
from .forms import FPForm

# Esta función solo comprueba si el usuario que quiere acceder es superusuario(admin).
def is_superuser(user):
    return user.is_superuser

# Cada función (def xxxx(request): ) representa una vista. La vista va a tener el nombre de la función.
# El parámetro request es necesario siempre en las vistas, ponérselo y listo.
def fp_list (request):
    # Para recuperar los FPs de la base de datos simplemente se llama al modelo FP y con el método .objects.all() se
    # obtienen todas las entradas que tenga la tabla FP. Luego siemplemente se devuelve un renderizado de la request con
    # el nombre del html creado en la carpeta /templates. A mayores se le puede pasar un objeto {} con datos. Por ejemplo
    # se podría pasar un {'title': 'Ejemeplo', 'fps': fps}. Esto haría que en el HTML se pueda llamar a un atributo llamado
    # title y fps y usarlos para pasarles datos o lo que haga falta.
    fps = FP.objects.all()

    fields = [field.verbose_name for field in FP._meta.fields]

    fps_data = [
        {field.name: getattr(fp, field.name) for field in FP._meta.fields}
        for fp in fps
    ]

    data = {
        'title': 'Ciclos formativos',
        'shortTitle': 'FP',
        'fps_data': fps_data,
        'fields': fields
    }
    
    return render(request, 'fp_list.html', data)

#@user_passes_test(is_superuser)
def add_fp (request):
    if request.method == 'POST':
        form = FPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fp_list')
    else:
        form = FPForm()

    return render(request, 'add_fp.html', {'form': form})