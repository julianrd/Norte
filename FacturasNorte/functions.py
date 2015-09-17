from time import strptime
from datetime import date

from django.core.exceptions import ObjectDoesNotExist, ValidationError

__author__ = 'Julian'

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core import mail
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from FacturasNorte.custom_classes import Factura
from FacturasNorte.models import Cliente, Empleado, Administrador, Historiales
from Norte import settings
from django import forms

from django.http import HttpRequest
from django.contrib.auth.models import User
from ipware.ip import get_ip



def crear_perfil(form, model):
    username = form.cleaned_data['email'].split("@")[0]
    #Nuevo Usuario
    nuevo_usuario = crear_usuario(form, model)
    #Nuevo_Perfil
    nuevo_perfil = crear_persona(form, model)

    if model == Administrador:
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = True
        password = form.cleaned_data['contrasena']
        permissions = []

    elif model == Empleado:
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = False
        password = form.cleaned_data['contrasena']
        permissions = settings.EMPLEADO_PERMISOS

    else:
        nuevo_usuario.is_staff = False
        nuevo_usuario.is_superuser = False
        password = User.objects.make_random_password()
        permissions = settings.CLIENTE_PERMISOS

    try:

        nuevo_usuario.set_password(password)
        nuevo_usuario.save()

        for perm in permissions:
            p = Permission.objects.get(codename=perm[0])
            nuevo_usuario.user_permissions.add(p)

        nuevo_usuario.save()
        nuevo_perfil.set_usuario(nuevo_usuario)
        nuevo_perfil.save()
        enviar_password(password)
        return

    except Exception:
        usuario_creado = get_object_or_404(User, username=username)
        usuario_creado.delete()
        raise ValidationError(('Campo invalido'), code='campos')

def crear_usuario(form, model):
    username = form.cleaned_data['email'].split("@")[0]
    nuevo_usuario = User()
    nuevo_usuario.username = username
    nuevo_usuario.email = form.cleaned_data['email']
    nuevo_usuario.is_active = True
    nuevo_usuario.date_joined = timezone.now()
    return nuevo_usuario

def crear_persona(form, model):
    persona = model()
    if model == Cliente:
        persona.set_dni(str(form.cleaned_data['nroDoc']))
    else:
        persona.set_dni(str(form.cleaned_data['dni']))
    persona.set_nombre(form.cleaned_data['nombre'])
    persona.set_email(form.cleaned_data['email'])
    persona.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
    persona.set_domicilio(form.cleaned_data['domicilio'])
    persona.set_telefono(form.cleaned_data['telefono'])
    return persona

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
    subject = subject.encode("utf-8")
    body = body.encode("utf-8")
    body = '{} ha enviado un email de contacto\n\n{}\n\n{}'.format(email, subject, body)
    send_mail(
        subject = 'Nuevo email de contacto',
        message = body,
        from_email = 'julian.rd7@gmail.com',
        recipient_list =['julian_rd7@hotmail.com'],
        )

def buscar_pdfs(pk, field=None, query=None):
     cliente = get_object_or_404(Cliente, nroUsuario=pk)
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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def crear_historial_correcto(user, request):

  nuevo_historial = Historiales()
  nuevo_historial.fecha = timezone.now()
  nuevo_historial.ip = get_client_ip(request)
  nuevo_historial.autenticado = 'Correcto'
  nuevo_historial.nroUsuario = user.id
  nuevo_historial.nombre = user.username

  if user.is_superuser:
      nuevo_historial.perfil = 'Admin'
  elif user.is_staff:
      nuevo_historial.perfil = 'Empleado'
  else:
      nuevo_historial.perfil = 'Cliente'

  nuevo_historial.save()

def crear_historial_incorrecto(request, form):


   nuevo_historial = Historiales()
   nuevo_historial.fecha = timezone.now()
   nuevo_historial.ip = get_client_ip(request)
   nuevo_historial.autenticado='Incorrecto'
   nuevo_historial.nroUsuario = ''
   nuevo_historial.nombre = form['email']
   nuevo_historial.save()


