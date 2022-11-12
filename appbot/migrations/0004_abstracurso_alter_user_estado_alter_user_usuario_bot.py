# Generated by Django 4.0.5 on 2022-08-01 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0003_alter_actividad_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstraCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_curso', models.IntegerField(null=True, verbose_name='id Curso')),
                ('nombre_curso', models.CharField(max_length=50, null=True, verbose_name='Nombre Curso')),
                ('id_nivel_tema', models.IntegerField(null=True, verbose_name='Orden')),
                ('categoria_nivel_tema', models.CharField(choices=[('Tema', 'Tema'), ('Subtema', 'Subtema'), ('SubSubtema', 'SubSubtema')], default='SubSubtema', max_length=10, null=True, verbose_name='Categoria Nivel Tema')),
                ('descripcion_nivel_tema', models.CharField(max_length=50, null=True, verbose_name='Dirección')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='estado',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Suspendido', 'Suspendido'), ('Inactivo', 'Inactivo')], db_index=True, default='Activo', max_length=12, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='user',
            name='usuario_bot',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Estudiante', 'Estudiante'), ('Docente', 'Docente'), ('Bot', 'Bot')], default='Estudiante', max_length=13, null=True, verbose_name='Usuario Bot'),
        ),
    ]