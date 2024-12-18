"""
URL configuration for eesn3_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('murosocial.urls')),
    path('', include('sistemausuarios.urls')),
]
"""




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('murosocial.urls'))
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")), # ésta url se encarga de 
    # recibir las direcciones de inicio de sesion, login, logout, cambio de contraseña
    # y tambien provee las vistas necesarias, lo unico q le falta es los html, los cuales
    # irán dentro de la carpeta template/registration.

    path("login/", include("login.urls")), #app encargada del manejo de usuarios.
]

# Si el depurador del proyecto está en True se agregará a las rutas los
# archivos de media, esto en el servidor no es necesario, ya que ya estarán asignadas las url para cargar los archivos de la carpeta "media"
if settings.DEBUG:
    from django.conf.urls.static import static
    # Acá se agrega a las urls del proyecto a la carpeta "media", así cuando querramos cargar un archivo de la media, éste se podrá 
    # visualizar correctamente.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # settings.MEDIA_URL, es la variable que tiene el nombre de la carpeta donde se almacenan los archivos de media 
    # settings.MEDIA_ROOT, es la ubicación de la carpeta de la carpeta donde se almacenarán los archivos de media
