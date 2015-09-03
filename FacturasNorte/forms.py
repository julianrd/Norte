# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login

__author__ = 'Julian'
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404

from FacturasNorte.functions import verificar_usuario

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


import datetime

from django.forms.extras.widgets import SelectDateWidget


class IniciarSesionForm(forms.Form):

    usuario = forms.EmailField(label='E-mail', show_hidden_initial='ejemplo@dominio.com')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), initial='')

    email = forms.EmailField(label='E-mail', show_hidden_initial='ejemplo@dominio.com')
    password = forms.CharField(label='Contrasena', widget=forms.PasswordInput(), initial='')
    captcha = NoReCaptchaField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('El email ingresado es incorrecto', code='email incorrecto')
        return email

    def clean_captcha(self):
        if not self.cleaned_data.get('captcha'):
            raise forms.ValidationError('Captcha no verificado, intente de nuevo', code='captcha')
        return self.cleaned_data.get('captcha')



def get_user(self):
        return get_object_or_404(User, email=self.cleaned_data['usuario'])

class AdminRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class':'special', 'size':'20'}))
    dni_field = forms.IntegerField(label='DNI', widget=forms.TextInput(attrs={'class': 'special', 'size':'20'}))
    email_field = forms.EmailField(label='Email')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', widget=SelectDateWidget())
    domicilio_field = forms.CharField(label='Domicilio', max_length=254)
    telefono_field = forms.CharField(label='Telefono', max_length=254)

    password_field = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(label='Repita Contraseña',widget=forms.PasswordInput(), initial='')

    password_field = forms.CharField( widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

    def clean_nombre_field(self):
        nombre = self.cleaned_data.get('nombre_field')

        if len(nombre) < 3:
            raise forms.ValidationError("el nombre debe contener mas caracteres")
        return nombre

    def clean_dni_field(self):
        dni = self.cleaned_data.get('dni_field')
        if dni > 99999999:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        elif dni < 2000000:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        return dni

    def clean_domicilio_field(self):
        domicilio = self.cleaned_data.get('domicilio_field')

        if len(domicilio) < 5:
            raise forms.ValidationError("el domicilio debe contener mas caracteres")
        return domicilio

    def clean_telefono_field(self):
        telefono = self.cleaned_data.get('telefono_field')

        if len(telefono) > 14:
            raise forms.ValidationError("El telefono debe tener un formato valido, ej: 3624XXYYZZ")
        return telefono

    def __init__(self, *args, **kwargs):
        super(AdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

    def clean(self):
        cleaned_data = super(AdminRegisterForm, self).clean()


        if verificar_usuario(self.cleaned_data['email_field'].split("@")[0]):
            password1 = self.cleaned_data.get('password_field')
            password2 = self.cleaned_data.get('password_again_field')

            if password1 and password1 != password2:
                raise forms.ValidationError("ContraseÃ±as no coinciden, vuelva a ingresar")

            return cleaned_data
        else:
            raise forms.ValidationError(('El email ingresado ya esta registrado'), code='email')

class EmpleadoRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class':'special', 'size':'20'}))
    dni_field = forms.IntegerField(label='DNI', widget=forms.TextInput(attrs={'class': 'special', 'size':'20'}))
    email_field = forms.EmailField(label='Email')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', widget=SelectDateWidget(years=range(1900, datetime.date.today().year-16)))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254)
    telefono_field = forms.CharField(label='Telefono', max_length=254)
    password_field = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(label='Repita contraseña', widget=forms.PasswordInput(), initial='')

    def clean_nombre_field(self):
        nombre = self.cleaned_data.get('nombre_field')

        if len(nombre) < 3:
            raise forms.ValidationError("el nombre debe contener mas caracteres")
        return nombre

    def clean_dni_field(self):
        dni = self.cleaned_data.get('dni_field')
        if dni > 99999999:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        elif dni < 2000000:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        return dni

    def clean_domicilio_field(self):
        domicilio = self.cleaned_data.get('domicilio_field')

        if len(domicilio) < 5:
            raise forms.ValidationError("el domicilio debe contener mas caracteres")
        return domicilio

    def clean_telefono_field(self):
        telefono = self.cleaned_data.get('telefono_field')

        if len(telefono) > 14:
            raise forms.ValidationError("El telefono debe tener un formato valido, ej: 3624XXYYZZ")
        return telefono


    def __init__(self, *args, **kwargs):
        super(EmpleadoRegisterForm, self).__init__(*args, **kwargs)

        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

    def clean(self):
        cleaned_data = super(EmpleadoRegisterForm, self).clean()


        if verificar_usuario(self.cleaned_data['email_field'].split("@")[0]):
            password1 = self.cleaned_data.get('password_field')
            password2 = self.cleaned_data.get('password_again_field')

            if password1 and password1 != password2:
                raise forms.ValidationError("ContraseÃ±as no coinciden, vuelva a ingresar")

            return cleaned_data
        else:
            raise forms.ValidationError(('El usuario ya existe'), code='usuario')



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


class ClienteRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class':'special', 'size':'20'}))
    dni_field = forms.IntegerField(label='DNI', widget=forms.TextInput(attrs={'class': 'special', 'size':'20'}))
    email_field = forms.EmailField(label='Email')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', widget=SelectDateWidget(years=range(1900, datetime.date.today().year-16)))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254)
    telefono_field = forms.CharField(label='Telefono', max_length=254)

    def clean_nombre_field(self):
        nombre = self.cleaned_data.get('nombre_field')

        if len(nombre) < 3:
            raise forms.ValidationError("el nombre debe contener mas caracteres")
        return nombre

    def clean_dni_field(self):
        dni = self.cleaned_data.get('dni_field')
        if dni > 99999999:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        elif dni < 2000000:
            raise forms.ValidationError("Formato DNI invalido, ingrese nuevamente")
        return dni

    def clean_domicilio_field(self):
        domicilio = self.cleaned_data.get('domicilio_field')

        if len(domicilio) < 5:
            raise forms.ValidationError("el domicilio debe contener mas caracteres")
        return domicilio

    def clean_telefono_field(self):
        telefono = self.cleaned_data.get('telefono_field')
        if len(telefono) > 14 or len(telefono) <= 9:
            raise forms.ValidationError("El telefono debe tener un formato valido, ej: 3624XXYYZZ")
        return telefono

    def clean(self):
        cleaned_data = super(ClienteRegisterForm, self).clean()
        if verificar_usuario(self.cleaned_data['email_field'].split("@")[0]):
            return cleaned_data
        else:
            raise forms.ValidationError(('El usuario ya existe'), code='usuario')


class CambiarContrasenaForm(forms.Form):
    contrasena_anterior = forms.CharField(label = "ContraseÃ±a Anterior", widget=forms.PasswordInput(), initial='')
    contrasena_nueva = forms.CharField(label = "ContraseÃ±a Nueva", widget=forms.PasswordInput(), initial='')
    confirmar_contrasena = forms.CharField(label = "Confirmar ContraseÃ±a",widget=forms.PasswordInput(), initial='')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CambiarContrasenaForm, self).__init__(*args, **kwargs)
        self.fields['contrasena_anterior'].required = False
        self.fields['contrasena_nueva'].required = False
        self.fields['confirmar_contrasena'].required = False
        self.user = user

    def clean(self):
        if self.user.check_password(self.cleaned_data.get('contrasena_anterior')):
            password1 = self.cleaned_data.get('contrasena_nueva')
            password2 = self.cleaned_data.get('confirmar_contrasena')
            if password1 and password1 != password2:
                raise forms.ValidationError("Las nuevas contraseÃ±as ingresadas no coinciden", code='match_passwords')
        else:
            raise forms.ValidationError("La contraseÃ±a anterior ingresada es invalida", code='old_password')
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

