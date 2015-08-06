__author__ = 'Julian'
from django import forms
from Norte import formats
from django.db import models

class AdminRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

class EmpleadoRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
    password_field = forms.CharField(widget=forms.PasswordInput(), initial='')
    password_again_field = forms.CharField(widget=forms.PasswordInput(), initial='')

<<<<<<< HEAD


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


=======
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields['password_field'].required = False
        self.fields['password_again_field'].required = False

    def clean(self):
        password1 = self.cleaned_data.get('password_field')
        password2 = self.cleaned_data.get('password_again_field')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class ClienteRegisterForm(forms.Form):
    nombre_field = forms.CharField(label='Nombre', initial='Su nombre')
    dni_field = forms.IntegerField(label='DNI', max_value=99999999, min_value=1000000, initial='00000000')
    email_field = forms.EmailField(label='Email', initial='ejemplo@dominio.com')
    fecha_nacimiento_field = forms.DateField(label='Fecha de Nacimiento', input_formats=formats.DATE_INPUT_FORMATS, widget=forms.DateInput(format= '%d-%m-%Y'))
    domicilio_field = forms.CharField(label='Domicilio', max_length=254, initial='Calle y altura')
    telefono_field = forms.CharField(label='Telefono', max_length=254, initial='Su numero sin comillas ni parentesis')
>>>>>>> ae52ab16a66f0f80fd83c1dd3516a3a34859e7fd

