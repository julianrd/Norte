# -*- coding: utf-8 -*-
__author__ = 'Julian'
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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

def validate_cuit(cuit):
    # validaciones minimas
    if len(cuit) != 11:
        raise ValidationError(u'El CUIT ingresado es inválido', code='cuit_invalido')

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])