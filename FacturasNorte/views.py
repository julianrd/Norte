from django.core import mail
from django.http import HttpResponse

__author__ = 'Julian'
from django.utils import timezone
from django import forms

<<<<<<< HEAD

from FacturasNorte.forms import AdminRegisterForm, ClienteRegisterForm
from FacturasNorte.models import Administrador, Cliente, Empleado
from FacturasNorte.models import User

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
=======
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629

from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
<<<<<<< HEAD

from django.views import generic
from . import models

=======
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629

#Importaciones para configuracion de contacto
import smtplib


#Importaciones para conficuracion de contacto

from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib import messages

<<<<<<< HEAD
=======
from FacturasNorte.forms import ClienteCambiarContrasenaForm, ContactUsuarioAnonimoForm, ContactUsuarioLoginForm, AdminRegisterForm, EmpleadoRegisterForm, ClienteRegisterForm
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629

from django.core.mail import send_mail

<<<<<<< HEAD
from FacturasNorte.models import Empleado

from FacturasNorte.forms import AdminRegisterForm, EmpleadoRegisterForm, ClienteRegisterForm
=======
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629
from FacturasNorte.models import Administrador, Empleado, Cliente
from FacturasNorte.models import User


@login_required
def index(request):
        return render(request, 'FacturasNorte/base/index.html')

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.

<<<<<<< HEAD


=======
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629
def ThankYou (request):
    return render (request, 'FacturasNorte/thankyou.html')


<<<<<<< HEAD

class AdminCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):

=======
class AdminCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629
    template_name = "FacturasNorte/admin/add_admin.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    permission_required = 'FacturasNorte.add_admin'

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = crear_usuario(form, 'admin')

        #Nuevo_Admin
        nuevo_admin = Administrador()
        nuevo_admin.set_dni(form.cleaned_data['dni_field'])
        nuevo_admin.set_nombre(form.cleaned_data['nombre_field'])
        nuevo_admin.set_email(form.cleaned_data['email_field'])
        nuevo_admin.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
        nuevo_admin.set_domicilio(form.cleaned_data['domicilio_field'])
        nuevo_admin.set_telefono(form.cleaned_data['telefono_field'])
        nuevo_admin.set_usuario(nuevo_usuario)
        nuevo_admin.save()

        return super(AdminCreateView, self).form_valid(form)

class AdminModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Administrador
    template_name = "FacturasNorte/admin/mod_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    permission_required = 'FacturasNorte.update_admin'

class AdminDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Administrador
    template_name = "FacturasNorte/admin/del_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.del_admin'

class AdminListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "FacturasNorte/admin/admin_list.html"
    model = Administrador
    context_object_name = 'admin_list'
    permission_required = 'FacturasNorte.view_admin'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Administrador.objects.all

class AdminDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/admin/admin_detail.html"
    model = Administrador
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.view_admin'

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EmpCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/admin/add_emp.html"
    form_class = EmpleadoRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    permission_required = 'FacturasNorte.add_empleado'

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = crear_usuario(form, 'empleado')

        #Nuevo Empleado
        nuevo_emp = Empleado()
        nuevo_emp.set_dni(form.cleaned_data['dni_field'])
        nuevo_emp.set_nombre(form.cleaned_data['nombre_field'])
        nuevo_emp.set_email(form.cleaned_data['email_field'])
        nuevo_emp.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
        nuevo_emp.set_domicilio(form.cleaned_data['domicilio_field'])
        nuevo_emp.set_telefono(form.cleaned_data['telefono_field'])
        nuevo_emp.set_usuario(nuevo_usuario)
        nuevo_emp.save()

        return super(EmpCreateView, self).form_valid(form)

class EmpModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    template_name = "FacturasNorte/admin/mod_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    permission_required = 'FacturasNorte.update_empleado'


class EmpDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Empleado
    template_name = "FacturasNorte/admin/del_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    context_object_name = 'empleado'
    permission_required = 'FacturasNorte.del_empleado'

class EmpListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "FacturasNorte/admin/emp_list.html"
    model = Empleado
    context_object_name = 'emp_list'
    permission_required = 'FacturasNorte.view_empleado'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Empleado.objects.all


class EmpDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/admin/emp_detail.html"
    model = Empleado
    context_object_name = 'empleado'
    permission_required = 'FacturasNorte.view_empleado'

    def get_context_data(self, **kwargs):
        context = super(EmpDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/empleado/add_cliente.html"
    form_class = ClienteRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.add_cliente'

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = crear_usuario(form, 'cliente')

        #Nuevo_Cliente
        nuevo_cliente = Cliente()
        nuevo_cliente.set_dni(str(form.cleaned_data['dni_field']))
        nuevo_cliente.set_nombre(form.cleaned_data['nombre_field'])
        nuevo_cliente.set_email(form.cleaned_data['email_field'])
        nuevo_cliente.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
        nuevo_cliente.set_domicilio(form.cleaned_data['domicilio_field'])
        nuevo_cliente.set_telefono(form.cleaned_data['telefono_field'])
        nuevo_cliente.set_usuario(nuevo_usuario)
        nuevo_cliente.save()

        return super(ClienteCreateView, self).form_valid(form)

class ClienteCambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/base/cambiar_contrasena.html"
    form_class = ClienteCambiarContrasenaForm
    success_url = reverse_lazy('FacturasNorte:cambiar_contrasena_hecho')
    permission_required = 'FacturasNorte.cambiar_cont_cliente'

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        c = super(FormView, self).get_context_data(**kwargs)
        c['user'] = self.request.user
        return c

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        usuario = self.get_context_data()['user']
        if usuario.check_password(form.cleaned_data['contrasena_anterior']):
            if form.cleaned_data['contrasena_nueva'] == form.cleaned_data['confirmar_contrasena']:
                usuario.set_password(form.cleaned_data['contrasena_nueva'])
                usuario.save()
                return super(ClienteCambiarContrasenaView, self).form_valid(form)
        else:
            raise forms.ValidationError("La contrasena anterior ingresada es invalida", code='old_password')

def cambiar_password_conf(request):
    return render(request, 'FacturasNorte/base/cambiar_contrasena_hecho.html', {})


class ClienteModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    template_name = "FacturasNorte/empleado/mod_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.modif_cliente'

class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cliente
    template_name = "FacturasNorte/empleado/del_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.del_cliente'

class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "FacturasNorte/empleado/cliente_list.html"
    model = Cliente
    context_object_name = 'cliente_list'
    permission_required = 'FacturasNorte.view_cliente'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Cliente.objects.all

class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/empleado/cliente_detail.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@login_required
def reset_password(request):
    usuario = request.user
    password = User.objects.make_random_password()
    usuario.set_password(password)
    enviar_password_regenerada(usuario, password)
    usuario.save()
    return render(request, 'FacturasNorte/cliente/reset_contrasena_hecho.html', {})

@login_required
def reset_password_conf(request):
    return render(request, 'FacturasNorte/cliente/reset_contrasena.html', {})

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            pass
    else:
        pass

def crear_usuario(form, rol):
    nuevo_usuario = User()
    nuevo_usuario.username = form.cleaned_data['email_field'].split("@")[0]
    nuevo_usuario.email = form.cleaned_data['email_field']
    nuevo_usuario.is_active = True
    nuevo_usuario.date_joined = timezone.now()

    if rol == 'admin':
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = True
        password = form.cleaned_data['password_field']

    elif rol == 'empleado':
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = False
        password = form.cleaned_data['password_field']

    elif rol == 'cliente':
        nuevo_usuario.is_staff = False
        nuevo_usuario.is_superuser = False
        password = User.objects.make_random_password()

    nuevo_usuario.set_password(password)
    enviar_password(password)
    nuevo_usuario.save()
    return nuevo_usuario

<<<<<<< HEAD


def send_email_contact(email, subject, body):
    import smtplib
    body = '{} ha enviado un email de contacto\n\n{}\n\n{}'.format(email, subject, body)
    send_mail(
        subject = 'Nuevo email de contacto',
        message = body,
        from_email = 'jor.lencina@gmail.com',
        recipient_list =['jor.lencina@gmail.com'],
            )


=======
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629
class ContactView(FormView):

    template_name = 'FacturasNorte/contact.html'
    success_url = reverse_lazy('FacturasNorte:thankyou')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.form_class = ContactUsuarioLoginForm
        else:
            self.form_class = ContactUsuarioAnonimoForm
        return super(ContactView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        body = form.cleaned_data.get('body')
        email = form.cleaned_data.get('email')

        if self.request.user.is_authenticated():
            send_email_contact(self.request.user.email, subject, body)

        else:
            send_email_contact(email, subject, body)
            messages.success(self.request, 'Email enviado con exito')


        return super(ContactView, self).form_valid(form)

def pdf_view(request):
    with open('C:\Users\Julian\Documents\Diario Norte\Proyecto Norte\PDFs\Hola.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed

<<<<<<< HEAD




def enviar_password(password):
    message = 'Su contrasena es: ' + str(password)
    sender = 'julian.rd7@gmail.com'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(sender, 'tel563539')
    server.sendmail(sender, ['julian_rd7@hotmail.com'], message)
    server.close()



=======
def enviar_password(password):
    message = 'Su contrasena es: ' + str(password)
    sender = 'julian.rd7@gmail.com'
>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629
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
        recipient_list =['julian_rd7@gmail.com'],
            )
<<<<<<< HEAD
=======


>>>>>>> 1b9d904f82a7210d44dc7c56447f4fa573275629



class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "FacturasNorte/home.html"
    paginate_by = 2

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "FacturasNorte/post.html"
