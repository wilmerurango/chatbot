# Generated by Django 4.0.5 on 2022-08-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0005_rename_usuario_bot_user_tipo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstracurso',
            name='nombre_nivel_tema',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='abstracurso',
            name='descripcion_nivel_tema',
            field=models.TextField(null=True, verbose_name='Descripción'),
        ),
    ]
