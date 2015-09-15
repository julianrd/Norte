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
from FacturasNorte.models import Cliente, Empleado
from Norte import settings

def crear_perfil(form, perfil):
    username = form.cleaned_data['email'].split("@")[0]
    #Nuevo Usuario
    nuevo_usuario = crear_usuario(form)

    if perfil == 'admin':
        #Nuevo_Perfil
        nuevo_perfil = crear_persona(form, Empleado)
        nuevo_perfil.set_admin(True)
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = True
        password = form.cleaned_data['contrasena']
        permissions = []

    elif perfil == 'empleado':
        #Nuevo_Perfil
        nuevo_perfil = crear_persona(form, Empleado)
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = False
        password = form.cleaned_data['contrasena']
        permissions = settings.EMPLEADO_PERMISOS

    else:
        #Nuevo_Perfil
        nuevo_perfil = crear_persona(form, Cliente)
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

def crear_usuario(form):
    username = form.cleaned_data['email'].split("@")[0]
    nuevo_usuario = User()
    nuevo_usuario.username = username
    nuevo_usuario.email = form.cleaned_data['email']
    nuevo_usuario.is_active = True
    nuevo_usuario.date_joined = timezone.now()
    return nuevo_usuario

def crear_persona(form, model):
    persona = model()
    persona.set_dni(str(form.cleaned_data['dni']))
    persona.set_nombre(form.cleaned_data['nombre'])
    persona.set_email(form.cleaned_data['email'])
    persona.set_fechaNacimiento(form.cleaned_data['fechaNacimiento'])
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
        subject = subject,
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
         if (doc == cliente.dni):
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
            return model.objects.filter(dni__icontains=int(searchQuery))
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

