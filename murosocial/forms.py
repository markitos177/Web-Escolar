from django import forms
from .models import Publicaciones

class EnviarCorreo(forms.Form):
    nombre = forms.CharField(label="Nombre completo", max_length=50,
                            #Cómo introducir 'Placeholder' en el formulario:
                            #Necesitaré usar 'widget' para manipular la renderización (también interacción) del campo
                            #Luego especifico el Input y le agrego el atributo
                            widget=forms.TextInput(attrs={'placeholder': 'Escriba aquí su nombre'})
                            )

    email = forms.EmailField(label="Ingrese su correo", max_length=50,
                            widget=forms.EmailInput(attrs={'placeholder': 'Escriba aquí su correo'})
                            )

    mensaje = forms.CharField(label="Escriba su mensaje...",
                            widget=forms.Textarea(attrs={'placeholder': 'Escriba aquí su mensaje'}),
                            max_length=255
                            )





######  AGREGADO  ######
class FormPublicacion(forms.ModelForm):
    titulo = forms.CharField(label="Título",
                            widget=forms.TextInput(attrs={"placeholder": "Título de la pulicación"}),
                            max_length=86,
                            )
    descripcion = forms.CharField(label="Descripción",
                            widget=forms.Textarea(attrs={"placeholder": "Descripción de la pulicación"}),
                            max_length=400,
                            )
    class Meta:
        model = Publicaciones
        fields = ["titulo", "descripcion"]
"""
    imagen1 = forms.ImageField(required=False)
    imagen2 = forms.ImageField(required=False)
    imagen3 = forms.ImageField(required=False)
"""
#Esto en teoría sería para que los campos de imagenes no sean requeridos
# pero ya le dí solución desde os campos del modelo

class FormEliminarNoticia(forms.Form):
    """LISTA = (
        (0, "Sin acción"),
        (1, "Eliminar los seleccionados"),
    )
    accion = forms.ChoiceField(label="Acción", choices=LISTA)"""
    pass