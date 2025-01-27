# El formulario es bastante completo, no hay que poner ni la mitad de las cosas para que funione
# bien, pero para que quede bonito :)

from django import forms

# Importamos el modelo para poder usarlo.
from .models import Module
from fp.models import FP
from fp.forms import FPForm


class ModuleForm(forms.ModelForm):
    # Se indica el modelo (FP) y los campos que queremos que tenga el formulario (en este caso todos).
    class Meta:
        model = Module
        fields = "__all__"
        labels = {
            "code": ("Código"),
            "name": ("Nombre"),
            "fp_id": ("Id de FP"),
        }
        # Aquí se pueden definir atributos como clases, placeholders etc. También se puede en el HTML.
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'ejemplo', 'placeholder': 'Indica el nombre del FP'}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "fp_id": forms.Select(attrs={"class": "form-control"}),
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
        }

    # Con esta función se coge el nombre del FP y se valida de la manera que se quiera. Longitud, si contiene una expresión regular...
    def clean_name(self):
        name = self.cleaned_data.get("name")

        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 5 caracteres.")

        return name
