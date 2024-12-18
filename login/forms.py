from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

#get_user_model: lo que hace es buscar en la variable "AUTH_USER_MODEL" del settings y retornar el model de usuarios

# "UserCreationFrom" es un formulario incluido en la librería de Django
# el cual te permite ingresar datos utiles para la creación de usuarios.
# En éste caso le agrego 2 campos más (email).
class FormCrearCuenta(UserCreationForm):
    email = forms.EmailField(label="Dirección de Correo", max_length=128)
    confir_email = forms.EmailField(label="Confirmar Dirección de Correo", max_length=128)

    username = forms.CharField(label="Nombre de usuario",
                               max_length=30,
                            )
    first_name = forms.CharField(label="Nombres",
                               max_length=30,
                            )
    last_name = forms.CharField(label="Apellidos",
                               max_length=30,
                            )
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "password1", "password2", "email", "confir_email"]
        # Tengo un dilema acá, ya que éste formulario, el cual viene de auth.forms, ya
        # tiene todos(o, la mayoría) de los campos que vamos a necesitar y sus respectivas
        # validaciones. Pero hay un PROBLEMA, y es que tiene un modelo base el cual
        # desde acá no se puede modificar, por eso está comentada la class Meta.
        # El modelo base que tiene es el de "User" el cual está en auth.models.User

        # SOLUCIÓN, lo que hice fue ir al auth.forms y modificar algunas cosas.



class FormCambiarDatos(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario",
                               max_length=30,
                               required=False,
                               widget=forms.TextInput(attrs={"placeholder": "Nombre de usuario"}),
                               help_text="*opcional",
                               )
    first_name = forms.CharField(label="Nombres",
                                max_length=30,
                                required=False,
                                widget=forms.TextInput(attrs={"placeholder": "Nombres"}),
                                help_text="*opcional",
                                )
    last_name = forms.CharField(label="Apellidos",
                                max_length=30,
                                required=False,
                                widget=forms.TextInput(attrs={"placeholder": "Apellidos"}),
                                help_text="*opcional",
                                )
    imagen = forms.ImageField(label="Foto de perfil", max_length=150, required=False, help_text="*opcional")
    #bio = forms.Textarea(attrs={"placeholder": "Descripcion sobre ti, qué te gusta o comó eres."})
    bio = forms.CharField(label="Biografía",
                          widget=forms.Textarea(attrs={"placeholder": "Descripcion sobre ti, qué te gusta o comó eres."}),
                          max_length=400,
                          required=False,
                          help_text="*opcional"
                          )
    email = forms.EmailField(label="Dirección de E-mail",
                             widget=forms.EmailInput(attrs={"placeholder": "Correo@gmail.com"}),
                             required=False,
                             max_length=150,
                             help_text="*opcional",
                             )
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "imagen", "bio"]

