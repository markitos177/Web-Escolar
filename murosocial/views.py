from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FormPublicacion
from .models import Publicaciones, Imagen
from eesn3_proyecto.settings import MEDIA_URL, MEDIA_ROOT
from login.models import UserPersonalizado
import time
import datetime
import os
import shutil

# get_user(request), lo que hace es tomar la request/peticion
# (se supone que ya debe estar logeada la request), y te
# devuelve una instancia del usuario, yo lo uso para crear publicaciones,

# Create your views here.

def index(request):
    publicaciones = Publicaciones.objects.filter(bloqueada=False)

    contexto = {
        "publicaciones": publicaciones,
        "MEDIA_URL": MEDIA_URL,
    }

    return render(request, "./app_murosocial/inicio.html", contexto)

def contacto(request):
    if request.method == "POST":
        instancia = forms.EnviarCorreo(request.POST)
        if instancia.is_valid():

            #//////////  Recolectar datos del formulario
            #Nombre completo del cliente
            nombre = instancia.cleaned_data['nombre']
            #Dirección de correo electrónico de quien me envía el mensaje
            remitente = instancia.cleaned_data['email']

            contenido = (
                    f"Nos has enviado un mensaje, a continuación la redacción del mismo:\n\n"
                    f"{instancia.cleaned_data['mensaje']}"
                )

            #////////// Preparación del envío de correo electrónico
            #Título del correo electrónico
            asunto = f"Mensaje de: {nombre}"
            #Destinatarios es el cuarto argumento obligatorio, el cual será una lista de correos electrónicos
            #Donde yo puedo enviar un mensaje a muchos de mis clientes. En este caso, a uno solo y es a mí
            destinatarios = ['juancampotc1@gmail.com']

            try:
                send_mail(asunto, contenido, remitente, destinatarios, fail_silently=True)
            except Exception:
                return HttpResponse("¡Ha ocurrido un error!")

            mensaje = {
                "titulo": "¡El correo electrónico ha sido enviado correctamente!",
                "texto": "Por favor, esté atento a su buzón de correos a la espera de una respuesta. \
                   \nMuchas gracias por comunicarte con nosotros"
            }
            ctx = {"mensaje": mensaje,
                   }

            return render(request, "./app_murosocial/redireccion_ok.html", ctx)

    instancia = forms.EnviarCorreo()
    ctx = {"instancia" : instancia}
    return render(request, "./app_murosocial/contacto.html", ctx)






#Aquí estamos definiendo un decorador llamado redirec, que toma una función func como argumento. Esta es la vista a la que se
#le aplicará este decorador. El propósito del decorador es modificar el comportamiento de esa vista (func).
def redirec(func):
    #El decorador devuelve una nueva función, llamada envoltura, que envuelve la función original (func). La función envoltura
    #recibe los #mismos parámetros que la vista original: request, *args (para cualquier argumento posicional) y **kwargs (para los argumentos clave).
    #En este punto, la función envoltura es la que realiza la validación y la redirección antes de llamar a la vista original.
    def envoltura(request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.is_staff:
            mensaje = {
                    "titulo": "Acceso denegado",
                    "texto": "No tienes acceso a ésta funcionalidad",
                    "url": "inicio",
                    "textolink": "Vuelve a la página Principal",
                }
            contexto = {
                "mensaje": mensaje
            }
            return render(request, "app_murosocial/redireccion_ok.html", contexto)  # Redirige a una pagina de error o una pagina de login con error q no es super usuario o del staff
        return func(request, *args, **kwargs)
    return envoltura

######  AGREGADO  ######
@login_required
@redirec
#@user_passes_test(funsion, login_url="direccion a donde queremos q lo lleve en caso q no sea super user") # por defecto redirecciona login_url="/accounts/login" q esta en settings.py sino se puede agregar a donde queremos q lo lleve con la misma variabe separada de una (,)
def nueva_noticia(request):
    if request.method == "POST":
        form = FormPublicacion(request.POST)
        imagenes = request.FILES.getlist("imagenes")

        if form.is_valid():
            form = form.cleaned_data
            ins_publicar = Publicaciones.objects.create(
                titulo = form["titulo"],
                descripcion = form["descripcion"],
                creador = request.user,
            )

            # Esto creará una carpeta para el usuario si es que éste no tiene. Aquí se almacenarán
            #todos los archivos que éste suba.
            
            if not os.path.exists(f"{MEDIA_ROOT}/users/{request.user.id}/img_noticias"):
                os.makedirs(f"{MEDIA_ROOT}/users/{request.user.id}/img_noticias")
            

            
            if imagenes:
                for img in imagenes:
                    img2 = str(img)
                    ruta = f"{MEDIA_ROOT}/users/{request.user.id}/img_noticias/{img2}"
                    #return HttpResponse(ruta.split("eesn3_proyecto")[1])
                    # Acá, a la hora de crear la instancia para cada img, éstas se almacenarán en la raíz de la carpeta
                    # media, inmediatamente esto sucede, dentro de la misma iteración del "for" donde creamos la imagen
                    # y es almacenada, proceso a mover la img a una nueva ubicación, esta nueva ubicación es la carpeta
                    # del usuario que creo la publicación y a donde irán a parar todas sus imgs
                    if img2.endswith(".jpg") or img2.endswith(".svg") or img2.endswith(".png") or img2.endswith(".jpeg"):
                        instancia = Imagen.objects.create(
                            imagen=img,
                            publicacion=ins_publicar,
                            url_absoluta= ruta.split("eesn3_proyecto")[1]
                        )
                        nombre = str(instancia.imagen)
                        
                        shutil.move(f"{MEDIA_ROOT}/{instancia.imagen}", f"{MEDIA_ROOT}/users/{request.user.id}/img_noticias/{nombre}")
            

            return redirect("inicio")

    else:
        form = FormPublicacion()

    contexto = {
        "form": form
    }
    return render(request, "app_murosocial/nueva-noticia.html", contexto)




@login_required
@redirec
def publicaciones(request, id_noticia):
    if request.method == "POST":

        hora = time.localtime()
        hora = datetime.datetime(
            hora[0], hora[1], hora[2], hora[3], hora[4], hora[5]
        )
        # El usuario accedería a ésta condicional, cuando está en la vista de eliminar noticia
        # y aprieta el enlance de "detalles de la publicación", el cual lo manda acá. El HTML de
        # ésta vista contiene un form con sólo un botón de eliminar. Cuando se aprieta el botón eliminar
        # la request estará enviando información al servidor mediante el "method==POST".

        #Como no sé qué publicación es la que está viendo el usuario(Y yo necesito darle la opción
        #de eliminarla), lo que hago es obtener la url de donde está ubicado el usuario, ya que la
        #url contiene el número de publicación.
        url = request.get_full_path_info().split("/")
        id_url = url[-1]

        noticia = Publicaciones.objects.get(id=id_url)
        noticia.bloqueada = True
        noticia.eliminador = request.user
        noticia.fecha_eliminacion = hora
        noticia.save()

        return redirect("eliminar-noticia")

    else:
        publicacion = Publicaciones.objects.get(id=id_noticia)
        bloqueo = publicacion.bloqueada
        if bloqueo == True:
            mensaje = {
                "titulo": "La Noticia ha sido eliminada",
                "texto": "Para poder visualizar la noticia diríjase a la página de recuperación",
                "url": "recuperar-noticia",
                "textolink": "Recuperar Noticias",
            }

            contexto = {
                "mensaje": mensaje,
            }
            return render(request, "app_murosocial/redireccion_ok.html", contexto)
    contexto = {
        "noticia": publicacion,
        "MEDIA_URL": MEDIA_URL,
    }
    return render(request, "app_murosocial/publicaciones.html", contexto)

@login_required
@redirec
def eliminar_noticia(request):
    if request.method == "POST":

        hora = time.localtime()
        hora = datetime.datetime(
                            hora[0], hora[1], hora[2], hora[3], hora[4], hora[5]
                        )
        parametros_usuario = request.POST

        publicaciones = Publicaciones.objects.filter(bloqueada=False)
        for fila in publicaciones:
            try:
                if parametros_usuario[f"{fila.id}"] == "on":
                    instancia = Publicaciones.objects.get(id=fila.id)
                    instancia.bloqueada = True
                    instancia.eliminador = request.user
                    instancia.fecha_eliminacion = hora
                    instancia.save()
            except:
                pass

        return redirect("eliminar-noticia")

    else:
        publicaciones = Publicaciones.objects.filter(bloqueada=False)
        contexto = {
            "publicaciones": publicaciones,
        }

    return render(request, "app_murosocial/eliminar_noticia.html", contexto)
@login_required
@redirec
def recuperar_noticia(request):
    if request.method == "POST":

        parametros_usuario = request.POST

        publicaciones = Publicaciones.objects.filter(bloqueada=True)
        for fila in publicaciones:

            try:
                if parametros_usuario[f"{fila.id}"] == "on":
                    instancia = Publicaciones.objects.get(id=fila.id)
                    instancia.bloqueada = False
                    instancia.eliminador = None
                    instancia.fecha_eliminacion = None
                    instancia.save()
            except:
                pass

        return redirect("recuperar-noticia")

    else:
        publicaciones = Publicaciones.objects.filter(bloqueada=True)
        contexto = {
            "publicaciones": publicaciones,
        }

    return render(request, "app_murosocial/recuperar_noticia.html", contexto)

@login_required
@redirec
def noticia_recuperar_detallada(request, id_noticia):
    if request.method == "POST":

        # El usuario accedería a ésta condicional, cuando está en la vista de recuperar notica
        # y aprieta el enlance de "detalles de la publicación", el cual lo manda acá. El HTML de
        # ésta vista contiene un form con sólo un botón de recuperar. Cuando se aprieta el botón recuperar
        # la request estará enviando información al servidor mediante el "method==POST".

        #Como no sé qué publicación es la que está viendo el usuario(Y yo necesito darle la opción
        #de recuperarña), lo que hago es obtener la url de donde está ubicado el usuario, ya que la
        #url contiene el número de publicación.
        url = request.get_full_path_info().split("/")
        id_url = url[-1]

        noticia = Publicaciones.objects.get(id=id_url)
        noticia.bloqueada = False
        noticia.eliminador = None
        noticia.fecha_eliminacion = None
        noticia.save()

        return redirect("recuperar-noticia")

    else:
        publicacion = Publicaciones.objects.get(id=id_noticia)
        bloqueada = publicacion.bloqueada
        if bloqueada == False:
            mensaje = {
                "titulo": "La Noticia ya ha sido recuperada",
                "texto": "Para poder eliminar la noticia diríjase a la página de eliminación",
                "url": "eliminar-noticia",
                "textolink": "Eliminar Noticias",
            }

            contexto = {
                "mensaje": mensaje,
            }
            return render(request, "app_murosocial/redireccion_ok.html", contexto)

    contexto = {
        "noticia": publicacion,
        "MEDIA_URL": MEDIA_URL,
    }
    return render(request, "app_murosocial/noticia-recuperar-detalles.html", contexto)

def creditos(request):
    #return redirect("creditos")

    contexto = {
        "MEDIA_URL": MEDIA_URL,
        }
    return render(request, "app_murosocial/creditos.html", contexto)