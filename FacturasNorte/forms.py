# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from FacturasNorte import config
from FacturasNorte.models import Empleado, Cliente, ClienteLegado
from FacturasNorte.validators import validate_emailExistente, validate_nombre, validate_dni, validate_domicilio, \
    validate_telefono, validate_cuit

__author__ = 'Julian'
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from Norte import settings
from FacturasNorte.functions import verificar_usuario

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


import datetime

from django.forms.extras.widgets import SelectDateWidget

class IniciarSesionForm(forms.Form):
    username = forms.CharField(label='Usuario o Email', show_hidden_initial='ejemplo@dominio.com',widget=forms.TextInput(attrs={'size': '30'}))
    password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput(attrs={'size': '30'}), initial='',)

    def get_user(self):
        return get_object_or_404(User, email=self.cleaned_data['usuario'])

class IniciarSesionCaptchaForm(forms.Form):
    username = forms.CharField(label='Usuario o Email', show_hidden_initial='ejemplo@dominio.com')
    password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput(), initial='')
    captcha = NoReCaptchaField(required=False)

    def get_user(self):
        return get_object_or_404(User, email=self.cleaned_data['usuario'])


class PersonaForm(forms.ModelForm):
    nombre = forms.CharField(validators=[validate_nombre], initial='')
    dni = forms.CharField(label='DNI', validators=[validate_dni], initial='')
    email = forms.EmailField(initial='')
    fechaNacimiento = forms.DateField(label='Fecha de nacimiento', widget=SelectDateWidget(years=range(1930, datetime.date.today().year+1)))
    domicilio = forms.CharField(validators=[validate_domicilio], initial='')
    telefono = forms.CharField(required=False, validators=[validate_telefono], initial='')

class EmpleadoForm(PersonaForm):
    
    class Meta:
        model = Empleado
        fields = ['nombre', 'dni', 'email', 'fechaNacimiento', 'domicilio', 'telefono']

class EmpleadoRegisterForm(EmpleadoForm):
    contrasena = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput(), initial='')
    confirmar_contrasena = forms.CharField(label=u'Confirmar contraseña', widget=forms.PasswordInput(), initial='')

    def clean(self):
        password1 = self.data['contrasena']
        password2 = self.data['confirmar_contrasena']
        if password1 and password1 != password2:
            raise forms.ValidationError(u"Contraseñas no coinciden, vuelva a ingresar")
        return super(EmpleadoRegisterForm, self).clean()

class ClienteForm(PersonaForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'dni', 'cuit', 'email', 'fechaNacimiento', 'domicilio', 'telefono')

class ClienteLegadoForm(forms.ModelForm):
    nombre = forms.CharField(validators=[validate_nombre])
    nroDoc = forms.CharField(label='CUIT', validators=[validate_cuit])
    email = forms.EmailField(validators=[validate_email])
    fechaNacimiento = forms.DateField(label='Fecha de nacimiento', widget=SelectDateWidget(years=range(1930, datetime.date.today().year+1)))
    domicilio = forms.CharField(validators=[validate_domicilio])
    telefono = forms.CharField(required=False, validators=[validate_telefono])

    class Meta:
        model = ClienteLegado
        fields = ('nombre', 'nroDoc', 'email', 'fechaNacimiento', 'domicilio', 'telefono')

class ContactUsuarioAnonimoForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        label='Asunto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class ContactUsuarioLoginForm(forms.Form):
    subject = forms.CharField(
        label='Asunto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class CambiarContrasenaForm(forms.Form):
    contrasena_anterior = forms.CharField(label = u'Contraseña anterior', widget=forms.PasswordInput())
    contrasena_nueva = forms.CharField(label = u'Contraseña nueva', widget=forms.PasswordInput())
    confirmar_contrasena = forms.CharField(label = u'Confirmar contraseña',widget=forms.PasswordInput())

    def clean(self):
        password2 = self.cleaned_data.get('confirmar_contrasena')
        password1 = self.cleaned_data.get('contrasena_nueva')
        if password1 and password1 != password2:
            raise forms.ValidationError(u"Las contraseñas ingresadas no coinciden", code='match_passwords')
        return self.cleaned_data

class RegenerarContrasenaForm(forms.Form):
    email = forms.EmailField(initial='ejemplo@dominio.com')

    def clean(self):
        try:
            User.objects.get(email=self.cleaned_data.get('username'))
        except ObjectDoesNotExist:
            raise forms.ValidationError("El username ingresado no se encuentra registrado")


class FiltroPersonaForm(forms.Form):
    query = forms.CharField(label='Buscar', show_hidden_initial='Ej. Messi')
    tipo = forms.ChoiceField(
                                required=True,
                                choices = ( ('nombre',u'Nombre'),
                                            ('dni',u'DNI'),
                                            ('username',u'Email'),
                                )
    )
    activo = forms.ChoiceField(label='Activo',
                               choices= ( (True, u'Si'),
                                          (False, u'No')
                               )
    )

class FiltroClienteForm(forms.Form):
    query = forms.CharField(label='Buscar', show_hidden_initial='Ej. Messi')
    tipo = forms.ChoiceField(
                                required=True,
                                choices = ( ('nombre',u'Nombre'),
                                            ('cuit', u'CUIT'),
                                            ('username',u'Email'),
                                )
    )
    activo = forms.ChoiceField(label='Activo',
                               choices= ( (True, u'Si'),
                                          (False, u'No')
                               )
    )

class FiltroFacturaForm(forms.Form):
    numero = forms.CharField(required=False, label='Nro', initial='')
    fecha = forms.DateField(required=False, label='Fecha', widget=SelectDateWidget(years=range(1995, datetime.date.today().year+1)))
    tipo = forms.ChoiceField(
                                required=True,
                                choices = ( ('1',u'Nro Factura'),
                                            ('2',u'Nro Pedido'),
                                            ('3',u'Fecha Factura'),
                                            ('4',u'Fecha Pedido'),
                                )
    )

class ConfigurationForm(forms.Form):
    pdf_root = forms.CharField(label='Carpeta PDFs',initial=config.PDF_ROOT,widget=forms.TextInput(attrs={'size': '40'}))
    carpeta_facturas = forms.CharField(label='Nombre carpeta de Facturas',initial=config.CARPETA_FACTURAS,widget=forms.TextInput(attrs={'size': '40'}))
    carpeta_pedidos = forms.CharField(label='Nombre carpeta de Pedidos',initial=config.CARPETA_PEDIDOS,widget=forms.TextInput(attrs={'size': '40'}))
    email_salida = forms.EmailField(label=u'Email para envíos', initial=config.EMAIL_SALIDA)
    email_entrada = forms.EmailField(label='Email para recepciones', initial=config.EMAIL_ENTRADA)

