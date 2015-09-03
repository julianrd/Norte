# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FacturasNorte', '0002_auto_20150901_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name_plural': 'Empleados', 'permissions': [('cambiar_cont', 'Puede cambiar su contrasena'), ('view_facturas', 'Puede ver las facutras de los clientes'), ('view_lista_cliente', 'Puede ver la lista de clientes'), ('view_detalle_cliente', 'Puede ver detalle cliente'), ('update_cliente', 'Puede modificar cliente'), ('agregar_cliente', 'Puede agregar cliente'), ('del_cliente', 'Puede eliminar cliente'), ('view_perfil_empleado', 'Puede ver su perfil de empleado')]},
        ),
    ]
