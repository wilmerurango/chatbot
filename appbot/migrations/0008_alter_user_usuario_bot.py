# Generated by Django 4.0.5 on 2022-06-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0007_alter_curtemstem_fecha_f_alter_curtemstem_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usuario_bot',
            field=models.CharField(choices=[('Si', 'Si'), ('No', 'no')], default='No', max_length=2, null=True, verbose_name='Usuario Bot'),
        ),
    ]
