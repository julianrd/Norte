# -*- coding: utf-8 -*-
__author__ = 'Julian'

from time import strptime
from datetime import date, datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, redirect

from FacturasNorte.models import Cliente, Empleado, Historiales, ClienteLegado, Historiales_registros
from Norte import settings

from django.utils import timezone

from django.contrib.auth.models import User

from FacturasNorte.models import Cliente, Empleado, Historiales, ClienteLegado, HistorialContrasena, Persona
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
        nuevo_perfil.set_activo(True)
        nuevo_perfil.save()
        enviar_password(password)
        return

    except Exception:
        usuario_creado = get_object_or_404(User, username=username)
        usuario_creado.delete()
        raise ValidationError((u'Campos invalidos'), code='campos')



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
    if model == Cliente:
        persona.set_cuit(str(form.cleaned_data['nroDoc']))
        dni = persona.get_cuit()[2:len(persona.get_cuit())-1]
        persona.set_dni(dni)
    else:
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

def obtener_fecha(fecha):
    fecstr = fecha[:2] + ' ' + fecha[2:4] + ' ' + fecha[4:8]
    fecha = strptime(fecstr, "%d %m %Y")
    fecha = date(fecha.tm_year, fecha.tm_mon, fecha.tm_mday)
    return fecha

def buscar_pdfs_pedidos(pk, field=None, pedido=None, factura=None, fechaFac=None, fechaPed=None):
     cliente = get_object_or_404(Cliente, nroUsuario=pk)
     storageManager = FileSystemStorage()
     facturas = storageManager.listdir(settings.PDF_FACTURAS)[1]
     pedidos = storageManager.listdir(settings.PDF_PEDIDOS)[1]
     PDFs = []

     if (field == 'fecha'):
        query = fechaPed
     else:
        query = pedido

     for ped in pedidos:
         cuit = ped.split('-')[1]
         if (cuit == cliente.cuit):
             nroPed = ped.split('-')[2]
             fechaPed = ped.split('-')[3].split('.')[0]
             fechaPed = obtener_fecha(fechaPed)

             if (field == None) or ((field == 'pedido') and (query == pedido)) or ((field == 'fechaPed') and (query == fechaPed)):
                 for fac in facturas:
                     pedido_factura = fac.split('-')[3]
                     if (nroPed == pedido_factura):
                         nroFac = fac.split('-')[2]
                         fechaFac = fac.split('-')[4].split('.')[0]
                         fechaFac = obtener_fecha(fechaFac)

                         pdf = PDF()
                         pdf.set_nroPedido(nroPed)
                         pdf.set_nroFactura(nroFac)
                         pdf.set_fechaPed(fechaPed)
                         pdf.set_fechaFac(fechaFac)
                         pdf.set_rutaFac('facturas/'+fac)
                         pdf.set_rutaPed('pedidos/'+ped)
                         PDFs.append(pdf)

     return PDFs


def reset_password(usuario, empleado):
    password = User.objects.make_random_password()
    usuario.set_password(password)
    registrar_cambio_contrasena(usuario, empleado)
    enviar_password_regenerada(usuario, password)
    usuario.save()
    return

def search_pdf_redirect(baseUrl, queryField, queryText):
    return redirect('/' + baseUrl + queryField + '=' + queryText)

def search_cliente(searchField, searchQuery, activo):
    if searchField == 'nombre':
        return Cliente.objects.filter(activo=activo, nombre__icontains=searchQuery)
    elif searchField == 'dni':
        return Cliente.objects.filter(activo=activo, dni__icontains=int(searchQuery))
    elif searchField == 'cuit':
        return Cliente.objects.filter(activo=activo, cuit__icontains=int(searchQuery))
    else:
        return Cliente.objects.filter(activo=activo, email__icontains=searchQuery)

def search_empleado(searchField, searchQuery, activo):
    if searchField == 'nombre':
        return Empleado.objects.filter(admin=True, activo=activo, nombre__icontains=searchQuery)
    elif searchField == 'dni':
        return Empleado.objects.filter(admin=True, activo=activo, dni__icontains=int(searchQuery))
    elif searchField == 'cuit':
        return Empleado.objects.filter(admin=True, activo=activo, cuit__icontains=int(searchQuery))
    else:
        return Empleado.objects.filter(admin=True, activo=activo, email__icontains=searchQuery)

def search_legado(searchField, searchQuery):
    if searchField == 'nombre':
        return ClienteLegado.objects.using('clientes_legados').filter(nombre__icontains=searchQuery)
    elif searchField == 'cuit':
        return ClienteLegado.objects.using('clientes_legados').filter(nroDoc__icontains=int(searchQuery))
    else:
        return ClienteLegado.objects.using('clientes_legados').filter(email__icontains=searchQuery)

def search_model(model, searchField, searchQuery, active, admin=False):

    if active == u'True':
        active = True
    else:
        active = False

    return model.filter(searchField, searchQuery, active, admin)

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

def crear_historial_correcto(user, request): #Se crea un historial de sesion, cuando se logean de manera correcta
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

def crear_historial_incorrecto(request, form):  #Se crea un historial de sesion, cuando se logean de manera erronea
   nuevo_historial = Historiales()
   nuevo_historial.fecha = timezone.now()
   nuevo_historial.ip = get_client_ip(request)
   nuevo_historial.autenticado='Incorrecto'
   nuevo_historial.nroUsuario = ''
   nuevo_historial.nombre = form['email']
   nuevo_historial.save()

def crear_historial_alta(form, user): #se crea un historial, por cada cliente que se da de alta
    historial_alta = Historiales_registros()
    historial_alta.cuit_cli = form.cleaned_data['nroDoc']
    historial_alta.nombre = form.cleaned_data['nombre']
    historial_alta.fecha = timezone.now()
    historial_alta.operador = user.username
    historial_alta.accion = 'Alta'
    historial_alta.save()


def crear_historial_baja(user, cliente): #se crea un historial, por cada cliente que se da de baja
    historial_baja = Historiales_registros()
    historial_baja.cuit_cli = cliente.get_cuit()
    historial_baja.nombre = cliente.get_nombre()
    historial_baja.fecha = timezone.now()
    historial_baja.operador = user.username
    historial_baja.accion = 'Baja'
    historial_baja.save()

def registrar_cambio_contrasena(usuario, empleado=None):
    try:
        persona = buscar_persona(usuario)
    except ObjectDoesNotExist:
        raise ValidationError('Ha ocurrido un error al buscar la persona')
    registro = HistorialContrasena()
    registro.nroUsuario = usuario.id
    registro.nombre = persona.nombre
    registro.email = persona.email
    registro.fecha = datetime.now()
    if empleado != None:
        registro.reestablecida_por_empleado = True
        registro.dni_empleado = empleado.dni
        registro.nombre_empleado = empleado.nombre
    else:
        registro.reestablecida_por_empleado = False
    try:
        registro.save()
    except Exception:
        raise ValidationError('Ha ocurrido un error al tratar de registrar su cambio')
    return

def buscar_persona(usuario):
    result = None
    try:
        result = Cliente.objects.get(email=usuario.email)
    except ObjectDoesNotExist:
        try:
            result = Empleado.objects.get(email=usuario.email)
        except ObjectDoesNotExist:
            pass
    finally:
        return result

