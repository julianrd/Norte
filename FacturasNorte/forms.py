from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

__author__ = 'Julian'
from django import forms
from Norte import formats
from django.db import models

class IniciarSesionForm(forms.Form):
    usuario = forms.EmailField(label='E-mail', show_hidden_initial='ejemplo@dominio.com')
    password = forms.CharField(label='Contrasena', widget=forms.PasswordInput(), initial='')

    def get_user(self):
        return get_object_or_404(User, email=self.cleaned_data['usuario'])

class AdminRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

    def __init__(self, *args, **kwargs):
        super(AdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

    def clean(self):
        password1 = self.cleaned_data.get('password_field')
        password2 = self.cleaned_data.get('password_again_field')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class EmpleadoRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

    def __init__(self, *args, **kwargs):
        super(EmpleadoRegisterForm, self).__init__(*args, **kwargs)

        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

    def clean(self):
        password1 = self.cleaned_data.get('password_field')
        password2 = self.cleaned_data.get('password_again_field')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

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
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')


class ClienteCambiarContrasenaForm(forms.Form):
    contrasena_anterior = forms.CharField(widget=forms.PasswordInput(), initial='')
    contrasena_nueva = forms.CharField(widget=forms.PasswordInput(), initial='')
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput(), initial='')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClienteCambiarContrasenaForm, self).__init__(*args, **kwargs)
        self.fields['contrasena_anterior'].required = False
        self.fields['contrasena_nueva'].required = False
        self.fields['confirmar_contrasena'].required = False
        self.user = user

    def clean(self):
        if self.user.check_password(self.cleaned_data.get('contrasena_anterior')):
            password1 = self.cleaned_data.get('contrasena_nueva')
            password2 = self.cleaned_data.get('confirmar_contrasena')
            if password1 and password1 != password2:
                raise forms.ValidationError("Las nuevas contrasenas ingresadas no coinciden", code='match_passwords')
            return self.cleaned_data
        else:
            raise forms.ValidationError("La contrasena anterior ingresada es invalida", code='old_password')
