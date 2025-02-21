# El formulario es bastante completo, no hay que poner ni la mitad de las cosas para que funione
# bien, pero para que quede bonito :)

from django import forms

from .models import Teacher, TeacherModule
from module.models import Module


class TeacherForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Teacher
        fields = "__all__"
        labels = {
            "name": ("Nombre"),
            "last_name": ("Apellidos"),
            "dni": ("DNI"),
            "email": ("Email"),
            "phone": ("Teléfono"),
            "modules": ("Módulos"),
        }
        # Aquí se pueden definir atributos como clases, placeholders etc. También se puede en el HTML.
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Indica el nombre del Profesor"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Indica los apellidos del Profesor"}
            ),
            "dni": forms.TextInput(attrs={"placeholder": "DNI"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email del Profesor"}),
            "phone": forms.TextInput(
                attrs={
                    "type": "phone",
                    "pattern": "[0-9]{9}",
                    "placeholder": "Teléfono del Profesor",
                }
            ),
        }
        # help_texts = {
        #     'name': 'Introduce el nombre del FP',
        #     'fp_type': 'Selecciona el tipo de FP',
        #     'description': 'Describe el FP de la mejor manera posible'
        # }

        # Aquí se establecen los mensajes de error que puede generar el formulario.
        error_messages = {
            "name": {
                "required": "El nombre es obligatorio.",
                "unique": "El nombre ya existe.",
            },
            "code": {
                "required": "El código es obligatorio.",
                "unique": "El código ya existe.",
            },
            "fp_id": {
                "required": "El FP es obligatorio.",
            },
            "codigo": {
                "required": "El código es obligatorio.",
                "unique": "El código ya existe.",
            },
            "nombre": {
                "required": "El nombre es obligatorio.",
                "unique": "El nombre ya existe.",
            },
            "creditos": {
                "required": "Los créditos son obligatorios.",
            },
            "profesor": {
                "required": "El profesor es obligatorio.",
            },
            "siglas": {
                "required": "Las siglas son obligatorias.",
                "unique": "Las siglas ya existen.",
            },
        }

    # Con esta función se coge el nombre del FP y se valida de la manera que se quiera. Longitud, si contiene una expresión regular...
    def clean_name(self):
        name = self.cleaned_data.get("name")

        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")

        return name

    def save(self, commit=True):
        teacher = super().save(commit=False)

        if commit:
            teacher.save()
            # Actualizamos la relación en la tabla intermedia
            selected_modules = self.cleaned_data["modules"]
            TeacherModule.objects.filter(teacher=teacher).delete()
            for module in selected_modules:
                TeacherModule.objects.create(
                    teacher=teacher, module=module, cursoEscolar="2024/25"
                )  # Puedes cambiar esto para que el usuario elija el curso escolar

        return teacher
