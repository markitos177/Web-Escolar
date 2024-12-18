from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

# Create your models here.
class UserPersonalizado(AbstractUser): # Acá heredamos todos los campos del modelo User de auth

    # Acá agregamos campos adicionales. Nota: éste nuevo modelo reemplazará al model auth.User
    imagen = models.ImageField(default='perfil-default.png', upload_to='')
    # default, es la ruta del archivo que aparecerá por defecto en este campo
    # upload_to, a la hora de que se suban archivos, éstos se guardarán en 
    # la carpeta especificada, en este caso sería "users/". Recordar que
    # todos estos archivos/carpetas estarán dentro de la carpeta "MEDIA", la
    # cual estará está definida en el settings
    bio = models.TextField(max_length=400, null=True, blank=True)

    # NOTA: Se pueden utilizar/modificar todos los campos de model User de auth, por ejemplo
    # modificar el campo de username

    # Tenía problemas con el related_name, el cual estaba en el campo groups, ya que no se
    # puede tener dos related_name con el mismo valor en dos tablas diferentes.
    # Al heredar todos los Campos de auth.User a este modelo, también heredaba el campo
    # groups el cual tenía el mismo related_name, entonces le cambio el nombre del related_name.
    groups = models.ManyToManyField(
        Group, # Acá va el nombre de la tabla a la cual estará vinculado éste campo mediante related_name
        related_name= "login_user_set", # mediante este nombre se podrá acceder al set de campos de la tabla User(osea, esta tabla) desde otra tabla que esté vinculada a ésta tabla(User)
        blank=True, # Si se borra aparecerá en blanco
    )

    # Acá pasa lo mismo que paso arriba
    user_permissions = models.ManyToManyField(
        Permission,
        related_name= "login_user_set",
        blank=True,
    )
    bloqueada = models.BooleanField(default=False)