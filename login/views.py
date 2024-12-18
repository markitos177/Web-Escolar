from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import FormCrearCuenta, FormCambiarDatos
from .models import UserPersonalizado
from eesn3_proyecto.settings import MEDIA_ROOT
import os
import shutil

# Create your views here.

# "logout" lo que hace es tomar como parámetro a "request"/peticion
# o "cliente", y cerrarle la sesión.

# "login_required", es un decorador que lo que hace es impedirle al
# cliente el acceso a una vista. Funciona como un decorador que va
# por encima de una función a la cual querramos que haga efecto.

def crear_cuenta(request):
    if request.method == "POST":
        """ la línea de abajo lo que hace es crear una instancia del
         formulario, y mediante "request.post", rellenar todos los
         campos del mismo. (3/11/24)"""

        # "param_inmuta", son todos los parámetros enviados mediante el método "POST" por el usuario.
        # éste es representado por un "QueryDic", el cual es un diccionario inmutable que contiene
        # todos los datos ingresados por el usuario. Es inmutable por defecto para garantizar 
        # que no se modifiquen de manera inadvertida los datos enviados por el usuario al servidor.
        param_inmuta = request.POST
        # "param_muta", es una copia "MUTABLE" del "QueryDic" recibido por parte del usuario.
        # con esto podés modificar esta copia sin afectar al original.
        param_muta = param_inmuta.copy()
        # "name", guardará el nombre de usuario ingresado.
        name = param_muta["username"].strip()
        # se cambia el valor ingresado por el usuario en el campo "username", reemplazamos los espacios
        # entre medio de las palabras por signos de "+", ya que sino el formulario arrojará un error en el campo
        # de "username". Ej, username="Prof Tevez Tomas", arrojaría error. Por eso se reemplazan los espacios por
        # signo "+". Más adelante a la hora de guardar los datos en la Base de Datos se reemplazan los signos "+"
        # por un espacio " ".
        param_muta["username"] = name.replace(" ", "+")
        # Ahora le indicamos que queremos crear una instancia de "FormCrearCuenta" y le pasamos como argumento
        # a "param_muta", y lo que hará será crear la instancia del formulario con todos los campos rellenados
        # por los datos que se encuentran dentro de la copia modificada del "QueryDic", el cual contiene los
        # datos ingresados por el usuario y el campo de "username" modificado para que no arroje error a la
        # hora de ingresar una cadena con espacio entre medio.
        form = FormCrearCuenta(param_muta)

        # "form.errors", lo que hace es similar a "form.is_valid", pero con la diferencia que "errors"
        # devuelve un diccionario con todos los errores que tenga los campos del formulario.
        # "is_valid", retorna un booleano, si algún campo del form tiene un error retornará False.
        errores = form.errors
        if form.is_valid():
            form = form.cleaned_data

            if form["email"] != form["confir_email"]:
                errores["email"] = "Has ingresado 2 Direcciones de Email diferentes"

                contexto = {
                    "error": errores
                }
                return render(request, "app_login/error.html", contexto)
            try:
                email = UserPersonalizado.objects.get(email=form["email"])
            except UserPersonalizado.DoesNotExist:
                pass
            else:
                errores["email"] = "El email ingresado está vinculado a otra cuenta. \
                    Por favor ingrese un Email nuevo"
                contexto = {
                    "error": errores,
                }
                return render(request, "app_login/error.html", contexto)
            UserPersonalizado.objects.create_user(
                username=form["username"].replace("+", " "),
                password=form["password1"],
                email=form["email"],
                first_name=form["first_name"],
                last_name=form["last_name"],
            )
            return redirect("inicio")
        else:
        
    
            contexto = {
                "error": errores,
            }
            return render(request, "app_login/error.html", contexto)
    else:
        form = FormCrearCuenta()
        contexto = {
            "form": form,
        }
        return render(request, "app_login/crear_cuenta.html", contexto)

@login_required
def cambiar_datos(request):
    if request.method == "POST":
        peticion = request.POST
        copia = peticion.copy()
        copia["username"] = copia["username"].strip().replace(" ", "+")
        copia["first_name"] = copia["first_name"].strip().replace(" ", "+")
        copia["last_name"] = copia["last_name"].strip().replace(" ", "+")
        form = FormCambiarDatos(copia)

        # request.FILES.getlist("campo"), lo que hace es traer una lista con todos los
        # archivos subidos en ese campo.
        imagenes = request.FILES.getlist("imagen")
        if imagenes:
            #acá lo que hago es convertir a str el archivo ingresado, así obtengo el nombre
            # del archivo para luego comparar en la condicional
            img = str(imagenes[0])
        errores = form.errors
        if form.is_valid():
            form = form.cleaned_data

            try:
                UserPersonalizado.objects.get(username=form["username"])
            except UserPersonalizado.DoesNotExist:
                pass
            else:
                errores["username"] = "El nombre de usuario ingresado ya está en uso."
                contexto = {
                    "error": errores
                }
                return render(request, "app_login/error.html", contexto)
           
            try:
                UserPersonalizado.objects.get(email=form["email"])
            except UserPersonalizado.DoesNotExist:
                pass
            else:
                errores["email"] = "El Email ingresado ya está vinculado a otra cuenta."
                contexto = {
                    "error": errores
                }
                return render(request, "app_login/error.html", contexto)
            

            usuario = UserPersonalizado.objects.get(id=request.user.id)
            # estas condicional de acá abajo siguen una lógica simple, la cual es la siguente:
            # si los campos del formulario no están vacíos, significa que el usuario ha ingresado
            # un dato, por lo tanto debe ser reemplazo el dato correspondiente del usuario por 
            # el nuevo dato ingresado en el formulario. En caso contrario, si los datos del form
            # están vacios, los datos del usuario no se reemplazan. Esto es posible gracias a
            # que los campos del formulario tiene "required=False
            if form["username"] != "":
                usuario.username = form["username"].replace("+", " ")

            if form["first_name"] != "":
                usuario.first_name = form["first_name"].replace("+", " ")

            if form["last_name"] != "":
                usuario.last_name = form["last_name"].replace("+", " ")
            
            if form["email"] != "":
                usuario.email = form["email"]

            # request.FILES.getlist("campo"), lo que hace es traer una lista con todos los
            # archivos subidos en ese campo.
            imagenes = request.FILES.getlist("imagen")
            if imagenes:
                #acá lo que hago es convertir a str el archivo ingresado, así obtengo el nombre
                # del archivo para luego comparar en la condicional
                img = str(imagenes[0])
                if img != "":
                    if not os.path.exists(f"{MEDIA_ROOT}/users/{request.user.id}/Perfil"):
                        os.makedirs(f"{MEDIA_ROOT}/users/{request.user.id}/Perfil")
                        
                    usuario.imagen = imagenes[0]

            if form["bio"] != "":
                usuario.bio = form["bio"]

            usuario.save()



            shutil.move(f"{MEDIA_ROOT}/{img}", f"{MEDIA_ROOT}/users/{request.user.id}/Perfil/{img}")
            return redirect("perfil")
        else:
            contexto = {
                "error": errores,
            }
            return render(request, "app_login/error.html", contexto)
    else:   
        form = FormCambiarDatos()
        contexto = {
            "form": form,
        }
        return render(request, "app_login/cambiar_datos.html", contexto)

def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")


@login_required
def perfil(request):
    return render(request, "app_login/perfil.html")