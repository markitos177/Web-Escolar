# Generated by Django 5.1.3 on 2024-12-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('murosocial', '0006_remove_imagen_nom_usuario_imagen_url_absoluta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='url_absoluta',
            field=models.CharField(max_length=150, null=True),
        ),
    ]