# Generated by Django 4.0.5 on 2022-11-15 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0029_conversacion_recurso_conversacion_recurso_dir_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsubtema',
            name='nombre',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre tema nivel tres'),
        ),
        migrations.AlterField(
            model_name='subtema',
            name='nombre',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre Subtema'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 15, 15, 18, 15, 346872), null=True, verbose_name='Fecha Creación'),
        ),
    ]
