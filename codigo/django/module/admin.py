from django.contrib import admin
from .models import Module, Enrolled
from teacher.models import TeacherModule


# Inline para TeacherModule (desde la perspectiva de Module)
class TeacherModuleInline(
    admin.TabularInline
):  # También puedes usar admin.StackedInline
    model = TeacherModule
    extra = (
        1  # Número de formularios vacíos que se muestran para añadir nuevas relaciones
    )


# Admin para Module
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "fp", "course")  # Campos a mostrar en la lista
    inlines = [TeacherModuleInline]  # Añade el inline para TeacherModule


# Registrar los modelos en el admin
admin.site.register(Module, ModuleAdmin)
admin.site.register(Enrolled)
