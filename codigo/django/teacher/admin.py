from django.contrib import admin
from .models import Teacher, TeacherModule


# Inline para TeacherModule
class TeacherModuleInline(
    admin.TabularInline
):  # También puedes usar admin.StackedInline
    model = TeacherModule
    extra = (
        1  # Número de formularios vacíos que se muestran para añadir nuevas relaciones
    )


# Admin para Teacher
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "last_name",
        "dni",
        "email",
        "phone",
    )  # Campos a mostrar en la lista
    inlines = [TeacherModuleInline]  # Añade el inline para TeacherModule


# Registrar los modelos en el admin
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherModule)
