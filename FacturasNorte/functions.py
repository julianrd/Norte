from time import strptime
from datetime import date
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q

__author__ = 'Julian'

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core import mail
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from FacturasNorte.custom_classes import Factura
from FacturasNorte.models import Cliente, Empleado
from Norte import settings

def crear_perfil(form, model):
    username = form.cleaned_data['email_field'].split("@")[0]
    #Nuevo Usuario
    nuevo_usuario = crear_usuario(form, 'cliente')
    #Nuevo_Perfil
    nuevo_model = model()
    nuevo_model.set_dni(str(form.cleaned_data['dni_field']))
    nuevo_model.set_nombre(form.cleaned_data['nombre_field'])
    nuevo_model.set_email(form.cleaned_data['email_field'])
    nuevo_model.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
    nuevo_model.set_domicilio(form.cleaned_data['domicilio_field'])
    nuevo_model.set_telefono(form.cleaned_data['telefono_field'])
    try:
        nuevo_model.set_usuario(nuevo_usuario)
        nuevo_model.save()
        enviar_password(nuevo_model.get_password)
        return nuevo_model
    except Exception:
        usuario_creado = get_object_or_404(User, username=username)
        usuario_creado.delete()
        raise ValidationError(('Campo invalido'), code='campos')

def crear_usuario(form, rol):
    username = form.cleaned_data['email_field'].split("@")[0]
    try:
        nuevo_usuario = User()
        nuevo_usuario.username = username
        nuevo_usuario.email = form.cleaned_data['email_field']
        nuevo_usuario.is_active = True
        nuevo_usuario.date_joined = timezone.now()

        if rol == 'admin':
            nuevo_usuario.is_staff = True
            nuevo_usuario.is_superuser = True
            password = form.cleaned_data['password_field']
            permissions = []

        elif rol == 'empleado':
            nuevo_usuario.is_staff = True
            nuevo_usuario.is_superuser = False
            password = form.cleaned_data['password_field']
            permissions = settings.EMPLEADO_PERMISOS

        elif rol == 'cliente':
            nuevo_usuario.is_staff = False
            nuevo_usuario.is_superuser = False
            password = User.objects.make_random_password()
            permissions = settings.CLIENTE_PERMISOS

        nuevo_usuario.set_password(password)
        nuevo_usuario.save()

        for perm in permissions:
            perm_object = Permission.objects.get(codename=perm[0])
            nuevo_usuario.user_permissions.add(perm_object)

        nuevo_usuario.save()
        return nuevo_usuario
    except Exception:
        return None

def enviar_password(password):
    message = 'Su contrasena es: ' + str(password)
    sender = 'julian.rd7@gmail.com'
    email = EmailMessage('Cuenta Registrada', message, sender,
            ['julian_rd7@hotmail.com'],
            headers = {'Reply-To': 'julian.rd7@gmail.com'})

    connection = mail.get_connection()
    connection.open()
    email.send()
    connection.close()

def enviar_password_regenerada(usuario, password):
    message = 'Senor/a usuario/a: ' + str(usuario.username) + '.' ' Su nueva contrasena es: ' + str(password)
    sender = 'julian.rd7@gmail.com'
    email = EmailMessage('Contrasena regenerada', message, sender,
            ['julian_rd7@hotmail.com'],
            headers = {'Reply-To': 'julian.rd7@gmail.com'})

    connection = mail.get_connection()
    connection.open()
    email.send()
    connection.close()

def send_email_contact(email, subject, body):
    body = '{} ha enviado un email de contacto\n\n{}\n\n{}'.format(email, subject, body)
    send_mail(
        subject = 'Nuevo email de contacto',
        message = body,
        from_email = 'julian.rd7@gmail.com',
        recipient_list =['julian_rd7@hotmail.com'],
            )

def buscar_pdfs(pk, field=None, query=None):
     cliente = get_object_or_404(Cliente, numero=pk)
     storageManager = FileSystemStorage()
     archivos = storageManager.listdir(settings.MEDIA_ROOT)[1]
     facturas = []
     if (field == 'fecha'):
                 query = strptime(query, "%Y-%m-%d")
                 query = date(query.tm_year, query.tm_mon, query.tm_mday)

     for a in archivos:
         doc = a.split('-')[1]
         if (doc == cliente.nroDoc):
             nroPed = a.split('-')[2]
             fec = a.split('-')[3].split('.')[0]
             fecstr = fec[:2] + ' ' + fec[2:4] + ' ' + fec[4:8]
             fec = strptime(fecstr, "%d %m %Y")
             fecha = date(fec.tm_year, fec.tm_mon, fec.tm_mday)

             if (field == None) or ((field == 'pedido') and (query == nroPed)) or ((field == 'fecha') and (query == fecha)):
                 f = Factura()
                 f.set_nroPedido(nroPed)
                 f.set_ruta(a)
                 f.set_fecha(fecha)
                 facturas.append(f)


     return facturas

def reset_password(usuario):
    password = User.objects.make_random_password()
    usuario.set_password(password)
    enviar_password_regenerada(usuario, password)
    usuario.save()
    return

def search_redirect(baseUrl, queryField, queryText):
    return redirect('/' + baseUrl + queryField + '=' + queryText)

def search_person(model, searchField, searchQuery):
    if searchField == 'nombre':
        return model.objects.filter(nombre__icontains=searchQuery)
    elif searchField == 'dni':
        if model == Cliente:
            return model.objects.filter(nroDoc__icontains=int(searchQuery))
        else:
            return model.objects.filter(dni__icontains=int(searchQuery))
    else:
        return model.objects.filter(email__icontains=searchQuery)

def verificar_usuario(username):
    try:
        User.objects.get(username=username)
        return False
    except ObjectDoesNotExist:
        return True