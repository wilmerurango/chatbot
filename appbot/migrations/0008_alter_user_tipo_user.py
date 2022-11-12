# Generated by Django 4.0.5 on 2022-08-01 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0007_alter_user_tipo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tipo_user',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Estudiante', 'Estudiante'), ('Docente', 'Docente'), ('Bot', 'Bot')], default='Estudiante', max_length=13, null=True, verbose_name='Tipo Usuario'),
        ),
    ]
