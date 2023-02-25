# Generated by Django 4.0.5 on 2023-02-25 20:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appbot', '0038_alter_user_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 25, 17, 52, 30, 974004), null=True, verbose_name='Fecha Creación'),
        ),
        migrations.CreateModel(
            name='UserActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_date', models.DateTimeField(null=True)),
                ('logout_date', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]