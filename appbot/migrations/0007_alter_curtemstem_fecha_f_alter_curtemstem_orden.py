# Generated by Django 4.0.5 on 2022-06-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0006_alter_curtemstem_fecha_f'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curtemstem',
            name='fecha_f',
            field=models.DateTimeField(verbose_name='Fecha Fin'),
        ),
        migrations.AlterField(
            model_name='curtemstem',
            name='orden',
            field=models.IntegerField(unique=True, verbose_name='Orden'),
        ),
    ]
