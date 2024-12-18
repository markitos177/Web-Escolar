from django.db import models
from login.models import UserPersonalizado

######  AGREGADO  ######
# Create your models here.
class Publicaciones(models.Model):
    titulo = models.CharField("Título de la publicación", max_length=86, default="titulo")
    descripcion = models.TextField(max_length=400, null=True)
    creador = models.ForeignKey(
        to=UserPersonalizado,
        related_name="publicado",
        on_delete=models.SET_NULL,
        null=True,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modificacion = models.DateTimeField(auto_now=True)
    bloqueada = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True)
    eliminador = models.ForeignKey(
        to=UserPersonalizado,
        on_delete=models.SET_NULL,
        null=True,
        related_name="publicacion_eliminada"
    )
    modificador = models.ForeignKey(
        to=UserPersonalizado,
        on_delete=models.SET_NULL,
        null=True,
        related_name="publicacion_modificada"
    )

class Imagen(models.Model):
    imagen = models.ImageField(null=True, blank=True, upload_to="")
    publicacion = models.ForeignKey(
        to=Publicaciones,
        related_name="imagenes",
        on_delete=models.SET_NULL,
        null=True,
    )
    url_absoluta = models.CharField(max_length=150, null=True)

    #blank=True, es para que acepte datos vacios a la hora de llenar el formularios.
    #null=True, es para que la tabla de la base de datos acepte campos vacíos.
    #upload_to, es, desde la carpeta "media", a donde se van a subir las imagenes.