# Generated by Django 4.0.5 on 2022-09-20 00:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0024_alter_prog_acti_estado_alter_user_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 19, 19, 52, 34, 235487), null=True, verbose_name='Fecha Creación'),
        ),
    ]
