import urlparse
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import Permission
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from FacturasNorte.custom_classes import  Factura, \
    CustomClienteDetailView, CustomAdminDetailView, CustomEmpleadoDetailView

__author__ = 'Julian'
from django.utils import timezone
from django import forms

from Norte import settings

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import login, logout, authenticate

from django.views import generic
from . import models

#Importaciones para conficuracion de contacto

from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib import messages

from FacturasNorte.forms import CambiarContrasenaForm, ContactUsuarioAnonimoForm, ContactUsuarioLoginForm, \
    IniciarSesionForm, FiltroNombreForm, RegenerarContrasenaForm

from django.core.mail import send_mail

from FacturasNorte.forms import AdminRegisterForm, EmpleadoRegisterForm, ClienteRegisterForm

from FacturasNorte.models import Administrador, Empleado, Cliente
from FacturasNorte.models import User

#Pruebas de Usuario
def is_admin(user):
    return user.is_superuser

def is_admin_o_emp(user):
    return user.is_superuser or user.is_staff

def is_emp(request):
    return request.user.is_staff

def is_admin_o_cliente(user):
    return user.is_superuser or not user.is_staff

class AdminTestRequiredMixin(object):
    @permission_required('is_superuser')
    def as_view(cls, **initkwargs):
        view = super(AdminTestRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class EmpleadoTestRequiredMixin(object):
    @staff_member_required
    def dispatch(self, *args, **kwargs):
        return super(EmpleadoTestRequiredMixin, self).dispatch(*args, **kwargs)

class FormListView(ListView, FormMixin):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


def base(request):
    return render(request, 'FacturasNorte/base/base.html')

@login_required
def index(request):
    return render(request, 'FacturasNorte/base/index.html')

class LoginView(FormView):
    form_class = IniciarSesionForm
    success_url = reverse_lazy('FacturasNorte:index')
    template_name = 'FacturasNorte/registration/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        user = authenticate(username=form.cleaned_data['usuario'], password=form.cleaned_data['password'])
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request,'FacturasNorte/registration/logged_out.html' )

def ThankYou (request):
    return render (request, 'FacturasNorte/thankyou.html')

class AdminPerfilView(LoginRequiredMixin, PermissionRequiredMixin, CustomAdminDetailView):
    template_name = "FacturasNorte/admin/perfil_admin.html"
    model = Administrador
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.view_admin'

class AdminCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
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


class AdminListView(LoginRequiredMixin, PermissionRequiredMixin, FormListView):
    template_name = "FacturasNorte/admin/admin_list.html"
    model = Administrador
    context_object_name = 'admin_list'
    permission_required = 'FacturasNorte.view_admin'

    form_class = FiltroNombreForm

    def form_valid(self, form):
        redirect('FacturasNorte:lista_cliente', {'query' : form.cleaned_data['query'],
                                                 'tipo': form.cleaned_data['tipo']})

    def get_queryset(self):
        try:
            query = self.request.POST['query']
            tipo = self.request.POST['tipo']
        except KeyError:
            return Administrador.objects.all()
        if tipo == '0':
            return Administrador.objects.filter(nombre__icontains=query)
        elif tipo == '2':
            return Administrador.objects.filter(email__icontains=query)
        else:
            return Administrador.objects.filter(dni__startswith=int(query))

class AdminDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/admin/admin_detail.html"
    model = Administrador
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.view_admin'

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EmpleadoPerfilView(LoginRequiredMixin, PermissionRequiredMixin, CustomEmpleadoDetailView):
    template_name = "FacturasNorte/empleado/perfil_emp.html"
    model = Empleado
    context_object_name = 'empleado'
    permission_required = 'FacturasNorte.view_empleado'

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

class EmpListView(LoginRequiredMixin, PermissionRequiredMixin, FormListView):
    template_name = "FacturasNorte/admin/emp_list.html"
    model = Empleado
    context_object_name = 'emp_list'
    permission_required = 'FacturasNorte.view_empleado'

    form_class = FiltroNombreForm

    def form_valid(self, form):
        redirect('FacturasNorte:lista_cliente', {'query' : form.cleaned_data['query'],
                                                 'tipo': form.cleaned_data['tipo']})

    def get_queryset(self):
        try:
            query = self.request.POST['query']
            tipo = self.request.POST['tipo']
        except KeyError:
            return Empleado.objects.all()
        if tipo == '0':
            return Empleado.objects.filter(nombre__icontains=query)
        elif tipo == '2':
            return Empleado.objects.filter(email__icontains=query)
        else:
            return Empleado.objects.filter(dni__startswith=int(query))

class EmpDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/admin/emp_detail.html"
    model = Empleado
    context_object_name = 'empleado'
    permission_required = 'FacturasNorte.view_empleado'

    def get_context_data(self, **kwargs):
        context = super(EmpDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ClientePerfilView(LoginRequiredMixin, PermissionRequiredMixin, CustomClienteDetailView):
    template_name = "FacturasNorte/cliente/perfil_cliente.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_cliente'

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

class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/base/cambiar_contrasena.html"
    form_class = CambiarContrasenaForm
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
                return super(CambiarContrasenaView, self).form_valid(form)
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

class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, FormListView):
    template_name = "FacturasNorte/empleado/cliente_list.html"
    model = Cliente
    context_object_name = 'cliente_list'
    paginate_by = 10
    permission_required = 'FacturasNorte.view_cliente'

    form_class = FiltroNombreForm

    def form_valid(self, form):
        redirect('FacturasNorte:lista_cliente', {'query' : form.cleaned_data['query'],
                                                 'tipo': form.cleaned_data['tipo']})

    def get_queryset(self):
        try:
            query = self.request.POST['query']
            tipo = self.request.POST['tipo']
        except KeyError:
            return Cliente.objects.all()
        if tipo == '0':
            return Cliente.objects.filter(nombre__icontains=query)
        elif tipo == '2':
            return Cliente.objects.filter(email__icontains=query)
        else:
            return Cliente.objects.filter(nroDoc__startswith=int(query))


class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/empleado/cliente_detail.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ClienteFacturasView(LoginRequiredMixin, PermissionRequiredMixin, CustomClienteDetailView):
    template_name = "FacturasNorte/cliente/facturas_list.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteFacturasView, self).get_context_data(**kwargs)
        context['lista_facturas'] = buscar_pdfs(self.kwargs.get(self.pk_url_kwarg))
        return context

class ClienteRegenerarContrasenaView(FormView):
    template_name = 'FacturasNorte/base/reset_contrasena_form.html'
    form_class = RegenerarContrasenaForm

    def form_valid(self, form):
        usuario = User.objects.get(email=form.cleaned_data['email'])
        reset_password(usuario)
        return render(self.request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})

@login_required
@user_passes_test(is_admin_o_emp)
def reset_password_view(request, pk):
    usuario = get_object_or_404(User,id=pk)
    reset_password(usuario)
    return render(request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})

@login_required
@user_passes_test(is_admin_o_emp)
def reset_password_conf(request, pk):
    try:
        usuario = get_object_or_404(Cliente, numero=pk).nroUsuario
    except ObjectDoesNotExist:
        try:
            usuario = get_object_or_404(Empleado, id=pk).nroUsuario
        except ObjectDoesNotExist:
            usuario = get_object_or_404(Administrador, id=pk).nroUsuario

    return render(request, 'FacturasNorte/base/reset_contrasena.html', {'usuario':usuario})

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
        permissions = []

    elif rol == 'empleado':
        nuevo_usuario.is_staff = True
        nuevo_usuario.is_superuser = False
        password = form.cleaned_data['password_field']
        permissions = Permission.objects.filter(Q(codename='view_empleado')| Q(codename__endswith='cliente'))

    elif rol == 'cliente':
        nuevo_usuario.is_staff = False
        nuevo_usuario.is_superuser = False
        password = User.objects.make_random_password()
        permissions = Permission.objects.filter(codename='view_cliente')

    nuevo_usuario.set_password(password)
    nuevo_usuario.save()
    enviar_password(password)

    for perm in permissions:
        nuevo_usuario.user_permissions.add(perm)

    nuevo_usuario.save()
    return nuevo_usuario

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

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "FacturasNorte/home.html"
    paginate_by = 2

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "FacturasNorte/post.html"

def buscar_pdfs(pk):
     cliente = get_object_or_404(Cliente, nroUsuario=pk)
     storageManager = FileSystemStorage()
     archivos = storageManager.listdir(settings.MEDIA_ROOT)[1]
     facturas = []

     for a in archivos:
         doc = a.split('-')[1]
         fec = a.split('-')[2].split('.')[0]
         if (doc == cliente.nroDoc):
             f = Factura()
             f.set_ruta(a)
             f.set_fecha(fec)
             facturas.append(f)

     return facturas

def reestablecer_password(request, pk):
    usuario = get_object_or_404(User, id=pk)
    reset_password(usuario)
    return render(request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})

def reset_password(usuario):
    password = User.objects.make_random_password()
    usuario.set_password(password)
    enviar_password_regenerada(usuario, password)
    usuario.save()
    return