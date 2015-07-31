__author__ = 'Julian'
from django import forms
from Norte import formats

class AdminRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

class ClienteRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

