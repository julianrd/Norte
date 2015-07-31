__author__ = 'Julian'
from django.test import TestCase
from django.contrib.auth.models import User

from FacturasNorte.models import Cliente, Administrador


class ClienteMethodTests(TestCase):

    def Cliente_tiene_usuario_normal_activo(self):
        test = True
        cliente = Cliente(nombre='Julian', email='julian.rd7@gmail.com', domicilio='vedia 417', telefono='154564549')
        try:
            u = cliente.get_usuario()
            if not u.is_active or u.is_superuser:
                test = False
        except User.DoesNotExist:
            test = False
        self.assertEqual(test, True)

    def Administrador_tiene_superusuario_activo(self):
        test = True
        cliente = Administrador(nombre='Julian', email='julian.rd7@gmail.com', domicilio='vedia 417', telefono='154564549')
        try:
            u = cliente.get_usuario()
            if not u.is_active or not u.is_superuser:
                test = False
        except User.DoesNotExist:
            test = False
        self.assertEqual(test, True)