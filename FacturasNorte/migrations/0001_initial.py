# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialContrasena',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nroUsuario', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=50)),
                ('username', models.EmailField(max_length=255, default='')),
                ('fecha', models.DateTimeField()),
                ('reestablecida_por_empleado', models.BooleanField(verbose_name='reestablecido por empleado', default=False)),
                ('dni_empleado', models.CharField(max_length=8, null=True)),
                ('nombre_empleado', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Cambio de contraseña',
                'verbose_name_plural': 'Cambios de contraseña',
                'db_table': 'Historiales_Contrasenas',
            },
            bases=(models.Model,),
        ),
    ]
