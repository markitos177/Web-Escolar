# Generated by Django 4.0.6 on 2024-11-29 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='titulo', max_length=86, verbose_name='Título de la publicación')),
                ('descripcion', models.TextField(max_length=400, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('modificacion', models.DateTimeField(auto_now=True)),
                ('bloqueada', models.BooleanField(default=False)),
                ('fecha_eliminacion', models.DateTimeField(null=True)),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publicado', to=settings.AUTH_USER_MODEL)),
                ('eliminador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publicacion_eliminada', to=settings.AUTH_USER_MODEL)),
                ('modificador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publicacion_modificada', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='users/')),
                ('publicacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='imagenes', to='murosocial.publicaciones')),
            ],
        ),
    ]
