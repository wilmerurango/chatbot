# Generated by Django 4.0.5 on 2022-09-18 23:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0023_alter_act_pregunta_opt_opt_correcta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prog_acti',
            name='estado',
            field=models.IntegerField(blank=True, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 18, 18, 18, 17, 874256), null=True, verbose_name='Fecha Creación'),
        ),
    ]