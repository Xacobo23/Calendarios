# El formulario es bastante completo, no hay que poner ni la mitad de las cosas para que funione
# bien, pero para que quede bonito :)

from django import forms

# Importamos el modelo para poder usarlo.
from .models import FP

class FPForm (forms.ModelForm):
    # Se indica el modelo (FP) y los campos que queremos que tenga el formulario (en este caso todos).
    class Meta:
        model = FP
        fields = ['name', 'fp_type', 'description']
        labels = {
            'name': ('Nombre'),
            'fp_type': ('Tipo'),
            'description': ('Descripción')
        }
        # Aquí se pueden definir atributos como clases, placeholders etc. También se puede en el HTML.
        widgets = {
            'name': forms.TextInput(attrs={'class': 'ejemplo', 'placeholder': 'Indica el nombre del FP'}),
            'fp_type': forms.Select(attrs={'class': 'ejemplo-select'}),
            'description': forms.Textarea(attrs={'class': 'ejemplo-textArea', 'rows': 5, 'placeholder': 'Descripción'})
        }
        # help_texts = {
        #     'name': 'Introduce el nombre del FP',
        #     'fp_type': 'Selecciona el tipo de FP',
        #     'description': 'Describe el FP de la mejor manera posible'
        # }

        # Aquí se establecen los mensajes de error que puede generar el formulario.
        error_messages = {
            'name': {
                'required': 'El nombre es obligatorio.',
                'max_length': 'El nombre es demasiado largo.'
            },
            'fp_type': {
                'required': 'Por favor, selecciona un tipo de FP.'
            },
        }
    
    # Con esta función se coge el nombre del FP y se valida de la manera que se quiera. Longitud, si contiene una expresión regular...
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 5 caracteres.')
        
        return name