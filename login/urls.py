from django.urls import path
from . import views

urlpatterns = [
    path("crear-cuenta", views.crear_cuenta, name="crear-cuenta"),
    path("cerrar-sesion", views.cerrar_sesion, name="cerrar-sesion"),
    path("perfil", views.perfil, name="perfil"),
    path("cambiar-datos", views.cambiar_datos, name="cambiar-datos"),
]