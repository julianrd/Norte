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
            name='Historiales_registros',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('cuit_cli', models.CharField(max_length=200)),
                ('nombre', models.CharField(blank=True, max_length=200)),
                ('fecha', models.DateTimeField(blank=True, max_length=200)),
                ('operador', models.CharField(blank=True, max_length=20)),
                ('accion', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Historial de Registro de Usuarios',
                'db_table': 'Historiales_registros',
                'verbose_name': 'Historiales_registros',
            },
            bases=(models.Model,),
        ),
    ]
