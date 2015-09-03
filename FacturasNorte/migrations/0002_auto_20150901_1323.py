# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FacturasNorte', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrador',
            options={'verbose_name_plural': 'Administradores', 'permissions': []},
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'permissions': [('cambiar_cont', 'Puede cambiar su contrasena'), ('view_perfil_cliente', 'Puede ver su perfil de cliente'), ('view_facturas_cliente', 'Puede ver sus facturas')]},
        ),
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name_plural': 'Empleados', 'permissions': [('cambiar_cont', 'Puede cambiar su contrasena'), ('view_facturas', 'Puede ver las facutras de los clientes'), ('view_lista_cliente', 'Puede ver la lista de clientes'), ('view_detalle_cliente', 'Puede ver detalle cliente'), ('update_cliente', 'Puede modificar cliente'), ('add_cliente', 'Puede agregar cliente'), ('del_cliente', 'Puede eliminar cliente'), ('view_perfil_empleado', 'Puede ver su perfil de empleado')]},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Novedad', 'verbose_name_plural': 'Novedades'},
        ),
    ]
