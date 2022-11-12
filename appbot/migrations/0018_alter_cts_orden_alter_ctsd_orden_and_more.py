# Generated by Django 4.0.5 on 2022-08-26 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0017_alter_prog_tem_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cts',
            name='orden',
            field=models.IntegerField(null=True, verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='ctsd',
            name='orden',
            field=models.IntegerField(null=True, verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='prog_sstem',
            name='orden',
            field=models.IntegerField(null=True, verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='prog_sstem',
            name='prog_Stem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='appbot.prog_stem', verbose_name='Progreso Detelle SubTema'),
        ),
        migrations.AlterField(
            model_name='prog_stem',
            name='orden',
            field=models.IntegerField(null=True, verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='prog_stem',
            name='prog_Tem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='appbot.prog_tem', verbose_name='Progreso SubTema'),
        ),
    ]