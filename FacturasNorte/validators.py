from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

__author__ = 'Julian'

def validate_nombre(nombre):
    if len(nombre) < 3:
        raise ValidationError("el nombre debe contener mas caracteres")

def validate_dni(dni):
        if int(dni) > 99999999:
            raise ValidationError("Formato DNI invalido, ingrese nuevamente")
        elif int(dni) < 2000000:
            raise ValidationError("Formato DNI invalido, ingrese nuevamente")

def validate_domicilio(domicilio):
    if len(domicilio) < 5:
        raise ValidationError("el domicilio debe contener mas caracteres")

def validate_telefono(telefono):
    if len(telefono) > 14 or len(telefono) <= 9:
        raise ValidationError("El telefono debe tener un formato valido, ej: 3624XXYYZZ")

def validate_emailExistente(email):
    try:
       User.objects.get(email=email)
    except ObjectDoesNotExist:
        raise ValidationError('El email ingresado es incorrecto', code='email incorrecto')
