# Generated by Django 5.1.3 on 2024-12-10 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('murosocial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
