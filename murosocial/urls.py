from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='inicio'),
    path("contacto", views.contacto, name='contacto'),
    path("nueva-noticia", views.nueva_noticia, name="nueva-noticia"),
    path("eliminar-noticia", views.eliminar_noticia, name="eliminar-noticia"),
    path("publicaciones/<int:id_noticia>", views.publicaciones, name="publicaciones"),
    path("recuperar-noticia", views.recuperar_noticia, name="recuperar-noticia"),
    path("recuperar-noticia-detalles/<int:id_noticia>", views.noticia_recuperar_detallada, name="detalles-recuperacion"),
    path("creditos", views.creditos, name='creditos'),
]