from django.test import TestCase
from django.views.generic.edit import FormMixin
from FacturasNorte import forms, functions

class AgregarUsuarioTests(TestCase, FormMixin):

    def agregar_admin_correcto(self):
        form_class = forms.EmpleadoRegisterForm
        data = {'nombre': 'julian ruiz diaz' , 'dni': '36017874', 'email': 'julian.rd7@gmail.com',
                'fechaNacimiento': '02/08/1992', 'domicilio': 'General Vedia 417', 'telefono': '3624563539',
                'contrasena': '1234NorteViejo', 'confirmar_contrasena': '1234NorteViejo'}
        form = form_class(data=data)
        form.is_valid()
        form.clean()
        self.assertEqual(functions.crear_perfil(form, 'admin'), True)


    def agregar_admin(self):
        form_class = forms.EmpleadoRegisterForm
        data = {'nombre':'julian ruiz diaz' , 'dni':'36017874', 'email':'julian.rd7@gmail.com',
                'fechaNacimiento':'02/08/1992', 'domicilio':'General Vedia 417', 'telefono':'3624563539',
                'contrasena':'1234NorteViejo', 'confirmar_contrasena':'1234NorteViejo'}
        form = form_class(data=data)
        form.is_valid()
        form.clean()
        functions.crear_perfil(form, 'admin')

