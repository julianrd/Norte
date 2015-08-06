__author__ = 'Julian'
from django.utils import timezone

from FacturasNorte.forms import AdminRegisterForm, ClienteRegisterForm
from FacturasNorte.models import Administrador, Cliente, Empleado
from FacturasNorte.models import User
from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


#Importaciones para conficuracion de contacto
import smtplib
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from .forms import ContactUsuarioAnonimoForm, ContactUsuarioLoginForm


from FacturasNorte.forms import AdminRegisterForm, ClienteRegisterForm
from FacturasNorte.models import Administrador, Cliente
from FacturasNorte.models import User




class AdminCreateView(FormView):
    template_name = "FacturasNorte/admin/add_admin.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_admin')

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

class AdminModifView(UpdateView):
    model = Administrador
    template_name = "FacturasNorte/admin/mod_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')

class AdminDeleteView(DeleteView):
    model = Administrador
    template_name = "FacturasNorte/admin/del_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')

class AdminListView(ListView):
    template_name = "FacturasNorte/admin/admin_list.html"
    model = Administrador
    context_object_name = 'admin_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Administrador.objects.all

class AdminDetailView(DetailView):
    template_name = "FacturasNorte/admin/admin_detail.html"
    model = Administrador
    context_object_name = 'admin'

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EmpCreateView(FormView):
    template_name = "FacturasNorte/staff/add_emp.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_emp')

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = User()
        nuevo_usuario.username = form.cleaned_data['email_field'].split("@")[0]
        nuevo_usuario.set_password(form.cleaned_data['password_field'])
        nuevo_usuario.email = form.cleaned_data['email_field']
        nuevo_usuario.is_active = True
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = True
        nuevo_usuario.date_joined = timezone.now()
        nuevo_usuario.save()

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

        return super(EmpCreateView, self).form_valid(form)


class EmpModifView(UpdateView):
    model = Empleado
    template_name = "FacturasNorte/empleado/mod_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_emp')

class EmpDeleteView(DeleteView):
    model = Empleado
    template_name = "FacturasNorte/empleado/del_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_emp')

class EmpListView(ListView):
    template_name = "FacturasNorte/empleado/emp_list.html"
    model = Empleado
    context_object_name = 'emp_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Empleados.objects.all

class EmpDetailView(DetailView):
    template_name = "FacturasNorte/empleado/emp_detail.html"
    model = Empleado
    context_object_name = 'empleados'

    def get_context_data(self, **kwargs):
        context = super(EmpDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ClienteCreateView(FormView):
    template_name = "FacturasNorte/empleado/add_cliente.html"
    form_class = ClienteRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_cliente')

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = crear_usuario(form, 'cliente')

        #Nuevo_Cliente
        nuevo_cliente = Cliente()
        nuevo_cliente.set_dni(form.cleaned_data['dni_field'])
        nuevo_cliente.set_nombre(form.cleaned_data['nombre_field'])
        nuevo_cliente.set_email(form.cleaned_data['email_field'])
        nuevo_cliente.set_fechaNacimiento(form.cleaned_data['fecha_nacimiento_field'])
        nuevo_cliente.set_domicilio(form.cleaned_data['domicilio_field'])
        nuevo_cliente.set_telefono(form.cleaned_data['telefono_field'])
        nuevo_cliente.set_usuario(nuevo_usuario)
        nuevo_cliente.save()

        return super(ClienteCreateView, self).form_valid(form)

class ClienteModifView(UpdateView):
    model = Cliente
    template_name = "FacturasNorte/empleado/mod_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "FacturasNorte/empleado/del_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')

class ClienteListView(ListView):
    template_name = "FacturasNorte/empleado/cliente_list.html"
    model = Cliente
    context_object_name = 'cliente_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Cliente.objects.all

class ClienteDetailView(DetailView):
    template_name = "FacturasNorte/empleado/cliente_detail.html"
    model = Cliente
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@login_required
def index(request):
        return render(request, 'FacturasNorte/base/index.html')

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

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.

"""
def crear_usuario(form, rol):
    nuevo_usuario = User()
    nuevo_usuario.username = form.cleaned_data['email_field'].split("@")[0]
    nuevo_usuario.email = form.cleaned_data['email_field']
    nuevo_usuario.is_active = True
    nuevo_usuario.date_joined = timezone.now()

    if rol == 'admin':
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = True
        nuevo_usuario.set_password(form.cleaned_data['password_field'])

    elif rol == 'empleado':
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = False
        nuevo_usuario.set_password(form.cleaned_data['password_field'])

    else:
        nuevo_usuario.is_staff = False
        nuevo_usuario.is_superuser = False
        password = User.objects.make_random_password()
        nuevo_usuario.set_password(password)
        send_mail('Cuenta registrada', 'Su contrasena es: ', 'from@example.com',
    ['to@example.com'], fail_silently=False)

    nuevo_usuario.save()
    return nuevo_usuario

"""


def send_email_contact(email, subject, body):
    import smtplib
    body = '{} ha enviado un email de contacto\n\n{}\n\n{}'.format(email, subject, body)
    send_mail(
        subject = 'Nuevo email de contacto',
        message = body,
        from_email = 'jor.lencina@gmail.com',
        recipient_list =['jor.lencina@gmail.com'],
            )



class ContactView(FormView):

    template_name = 'FacturasNorte/contact.html'
    success_url = reverse_lazy('contact.html')

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


