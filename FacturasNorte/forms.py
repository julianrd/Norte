# -*- coding: utf-8 -*-
from django.core.validators import validate_email
from FacturasNorte.models import Empleado, Cliente
from FacturasNorte.validators import validate_emailExistente, validate_nombre, validate_dni, validate_domicilio, \
    validate_telefono

__author__ = 'Julian'
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from FacturasNorte.functions import verificar_usuario

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


import datetime

from django.forms.extras.widgets import SelectDateWidget


class IniciarSesionForm(forms.Form):
    email = forms.EmailField(label='E-mail', show_hidden_initial='ejemplo@dominio.com', validators=[validate_emailExistente])
    password = forms.CharField(label='Contrasena', widget=forms.PasswordInput(), initial='')
    captcha = NoReCaptchaField(required=False)

    def clean_captcha(self):
        if not self.cleaned_data.get('captcha'):
            raise forms.ValidationError('Captcha no verificado, intente de nuevo', code='captcha')
        return self.cleaned_data.get('captcha')

    def get_user(self):
        return get_object_or_404(User, email=self.cleaned_data['usuario'])

class PersonaForm(forms.ModelForm):
    nombre = forms.CharField(validators=[validate_nombre])
    dni = forms.CharField(validators=[validate_dni])
    email = forms.EmailField(validators=[validate_email])
    fechaNacimiento = forms.DateField(widget=SelectDateWidget(years=range(1930, datetime.date.today().year+1)))
    domicilio = forms.CharField(validators=[validate_domicilio])
    telefono = forms.CharField(validators=[validate_telefono])


class EmpleadoForm(PersonaForm):

    class Meta:
        model = Empleado
        fields = ['nombre', 'dni', 'email', 'fechaNacimiento', 'domicilio', 'telefono']


class EmpleadoRegisterForm(EmpleadoForm):
    confirmar_contrasena = forms.CharField(label = "Confirmar contraseña", widget=forms.PasswordInput(), initial='')

    def clean(self):
        cleaned_data = super(EmpleadoRegisterForm, self).clean()

        try:
            if verificar_usuario(self.cleaned_data['email'].split("@")[0]):
                password1 = self.cleaned_data.get('contrasena')
                password2 = self.cleaned_data.get('confirmar_contrasena')

                if password1 and password1 != password2:
                    raise forms.ValidationError("Contraseñas no coinciden, vuelva a ingresar")
            else:
                raise forms.ValidationError(('El usuario ya existe'), code='usuario')
        except:
            pass
        return cleaned_data

class ClienteForm(PersonaForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'dni', 'email', 'fechaNacimiento', 'domicilio', 'telefono')


class ClienteUpdateForm(ClienteForm):
    contrasena = forms.CharField(label = "Contraseña", widget=forms.PasswordInput(), initial='')

    def clean(self):
        try:
            cleaned_data = super(ClienteUpdateForm, self).clean()
            if not verificar_usuario(self.cleaned_data['email'].split("@")[0]):
                raise forms.ValidationError(('El usuario ya existe'), code='usuario')
        except KeyError:
            pass
        return cleaned_data

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
    contrasena_anterior = forms.CharField(label = "Contraseña anterior", widget=forms.PasswordInput())
    contrasena_nueva = forms.CharField(label = "Contraseña nueva", widget=forms.PasswordInput())
    confirmar_contrasena = forms.CharField(label = "Confirmar contraseña",widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CambiarContrasenaForm, self).__init__(*args, **kwargs)
        self.fields['contrasena_anterior'].required = False
        self.fields['contrasena_nueva'].required = False
        self.fields['confirmar_contrasena'].required = False
        self.user = user
        return

    def clean_confirmar_contrasena(self):
        if self.user.check_password(self.cleaned_data.get('contrasena_anterior')):
            password1 = self.cleaned_data.get('contrasena_nueva')
            password2 = self.cleaned_data.get('confirmar_contrasena')
            if password1 and password1 != password2:
                raise forms.ValidationError("Las nuevas contraseñas ingresadas no coinciden", code='match_passwords')
        else:
            if self.cleaned_data.get('contrasena_anterior') != '':
                raise forms.ValidationError("La contraseña anterior ingresada es invalida", code='old_password')
        return self.cleaned_data

class RegenerarContrasenaForm(forms.Form):
    email = forms.EmailField(initial='ejemplo@dominio.com')

    def clean(self):
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except ObjectDoesNotExist:
            raise forms.ValidationError("El email ingresado no se encuentra registrado")


class FiltroPersonaForm(forms.Form):
    query = forms.CharField(label='Buscar', initial='Ej. Messi')
    tipo = forms.ChoiceField(
                                required=True,
                                choices = ( ('nombre',u'Nombre'),
                                            ('dni',u'DNI'),
                                            ('email',u'Email'),
                                )
    )

class FiltroFacturaForm(forms.Form):
    pedido = forms.CharField(required=False, label='Nro Pedido', initial='')
    fecha = forms.DateField(required=False, label='Fecha', widget=SelectDateWidget(years=range(1995, datetime.date.today().year+1)))
    tipo = forms.ChoiceField(
                                required=True,
                                choices = ( ('pedido',u'Pedido'),
                                            ('fecha',u'Fecha'),
                                )
    )

