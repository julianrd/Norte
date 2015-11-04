# -*- coding: utf-8 -*-

#import urllib.parse

from datetime import date, datetime
import urlparse
from django.core.files import File

from Norte import settings


from datetime import date
import urlparse

from django.core.files.storage import default_storage

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from django.utils import timezone
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import generic


from FacturasNorte.custom_classes import CustomClienteDetailView, CustomAdminDetailView, CustomEmpleadoDetailView, \
    LogicDeleteView, FormListView
from FacturasNorte.functions import send_email_contact, reset_password, \
    crear_perfil, search_model, buscar_pdfs_pedidos, registrar_cambio_contrasena, crear_historial_alta, buscar_pdfs_facturas, \
    get_client_ip, iniciar_sesion, corregir_fecha_update
from FacturasNorte import config

from . import models

from django.shortcuts import render_to_response



from django.template import RequestContext


#Importaciones para conficuracion de contacto

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages

from FacturasNorte.forms import CambiarContrasenaForm, ContactUsuarioAnonimoForm, ContactUsuarioLoginForm, \
    IniciarSesionForm, RegenerarContrasenaForm, FiltroPersonaForm, FiltroFacturaForm, ClienteForm, \
    EmpleadoForm, ClienteLegadoForm, FiltroClienteForm, IniciarSesionCaptchaForm, ConfigurationForm

from FacturasNorte.forms import  EmpleadoRegisterForm
from FacturasNorte.models import Empleado, Cliente, ClienteLegado, Historiales
from FacturasNorte.models import User
from FacturasNorte.functions import crear_historial_correcto, crear_historial_incorrecto

#Pruebas de Usuario
def is_admin_o_emp(user):
    return user.is_superuser or user.is_staff

def base(request):
    return render(request, 'FacturasNorte/base/base.html')

@login_required
def index(request):
    return render(request, 'FacturasNorte/base/index.html')

class LoginView(FormView):
    form_class = IniciarSesionCaptchaForm
    success_url = reverse_lazy('FacturasNorte:index')
    template_name = 'FacturasNorte/registration/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        self.form_class = IniciarSesionForm
        return self.form_class

    def get_context_data(self, **kwargs):
        time = timezone.now() - timezone.timedelta(minutes=1)
        ip = get_client_ip(self.request)
        query = Historiales.objects.filter(autenticado='Incorrecto', ip=ip, fecha__gte=time)
        if query:
            kwargs['captcha'] = True
        else:
            kwargs['captcha'] = False
        return super(LoginView, self).get_context_data(**kwargs)


    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        try:
            #Captcha activo
            if form.data['g-recaptcha-response'] != '':
                try:
                    username = str(form.cleaned_data['username'])
                    password = str(form.cleaned_data['password'])
                    user = authenticate(username=username, password=password)
                    login(self.request, user)
                    crear_historial_correcto(user, self.request)

                except Exception:
                    form.add_error('password', ValidationError('Contrasena incorrecta', code='authentication'))
                    crear_historial_incorrecto(self.request, form.cleaned_data)
                    return self.form_invalid(form)

                return HttpResponseRedirect(self.get_success_url())

            else:
                crear_historial_incorrecto(self.request, form.cleaned_data)
                form.add_error ('password', ValidationError('Captcha incorrecto', code='captcha'))
                return self.form_invalid(form)

        except MultiValueDictKeyError:
            #Captcha inactivo
            try:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(self.request, user)
                crear_historial_correcto(user, self.request)

            except Exception:
                form.add_error('password', ValidationError('Contrasena incorrecta', code='authentication'))
                crear_historial_incorrecto(self.request, form.cleaned_data)
                return self.form_invalid(form)

            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        #redirect_to_string = str(redirect_to)
        #netloc = urllib.parse.urlsplit(redirect_to_string)[1]
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

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, error=True))

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request,'FacturasNorte/registration/logged_out.html')

def ThankYou (request):
    return render (request, 'FacturasNorte/thankyou.html')

class AdminPerfilView(LoginRequiredMixin, PermissionRequiredMixin, CustomAdminDetailView):
    template_name = "FacturasNorte/admin/perfil_admin.html"
    model = Empleado
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.view_admin'

class AdminCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/admin/add_admin.html"
    form_class = EmpleadoRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    permission_required = 'FacturasNorte.add_admin'

    def form_valid(self, form):
        crear_perfil(form, 'admin')
        return super(AdminCreateView, self).form_valid(form)

class AdminModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "FacturasNorte/admin/mod_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    permission_required = 'FacturasNorte.update_admin'


class AdminDeleteView(LoginRequiredMixin, PermissionRequiredMixin, LogicDeleteView):
    model = Empleado
    template_name = "FacturasNorte/admin/del_admin.html"
    success_url = reverse_lazy('FacturasNorte:lista_admin')
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.del_admin'


class AdminListView(LoginRequiredMixin, PermissionRequiredMixin, FormListView):
    template_name = "FacturasNorte/admin/admin_list.html"
    model = Empleado
    context_object_name = 'admin_list'
    permission_required = 'FacturasNorte.view_admin'
    form_class = FiltroPersonaForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(AdminListView, self).get_initial()
        try:
            initial['query'] = self.request.GET['query']
            initial['tipo'] = self.request.GET['tipo']
            initial['activo'] = self.request.GET['activo']
        finally:
            return initial

    def get_queryset(self):
        try:
            return search_model(Empleado,self.request.GET['tipo'], self.request.GET['query'], u'True', True)
        except KeyError:
            return Empleado.objects.filter(activo=True, admin=True)

class AdminDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/admin/admin_detail.html"
    model = Empleado
    context_object_name = 'admin'
    permission_required = 'FacturasNorte.view_admin'

    def get_queryset(self):
       return Empleado.objects.filter(admin=True)

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EmpleadoPerfilView(LoginRequiredMixin, PermissionRequiredMixin, CustomEmpleadoDetailView):
    template_name = "FacturasNorte/empleado/perfil_emp.html"
    model = Empleado
    context_object_name = 'empleado'
    permission_required = 'FacturasNorte.view_perfil_empleado'

class EmpCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    model = Empleado
    form_class = EmpleadoRegisterForm
    template_name = "FacturasNorte/admin/add_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    permission_required = 'FacturasNorte.add_empleado'

    def form_valid(self, form):
        crear_perfil(form, 'empleado')
        return super(EmpCreateView, self).form_valid(form)

class EmpModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "FacturasNorte/admin/mod_emp.html"
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    permission_required = 'FacturasNorte.view_perfil_empleado'

class EmpModifPerfilView(EmpModifView):
    template_name = 'FacturasNorte/empleado/mod_perfil_emp.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('FacturasNorte:perfil_empleado', kwargs={'pk' : self.request.user.id})
        return super(EmpModifPerfilView, self).form_valid(form)

class EmpDeleteView(LoginRequiredMixin, PermissionRequiredMixin, LogicDeleteView):
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
    form_class = FiltroPersonaForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(EmpListView, self).get_initial()
        try:
            initial['query'] = self.request.GET['query']
            initial['tipo'] = self.request.GET['tipo']
            initial['activo'] = self.request.GET['activo']
        finally:
            return initial

    def get_queryset(self):
        try:
            return search_model(Empleado, self.request.GET['tipo'], self.request.GET['query'], u'True', False)
        except KeyError:
            return Empleado.objects.filter(activo=True, admin=False)

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
    permission_required = 'FacturasNorte.view_perfil_cliente'

class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/base/cambiar_contrasena.html"
    form_class = CambiarContrasenaForm
    success_url = reverse_lazy('FacturasNorte:cambiar_contrasena_hecho')
    permission_required = 'FacturasNorte.cambiar_cont'

    def form_valid(self, form):
        if not self.request.user.check_password(form.cleaned_data.get('contrasena_anterior')):
            form.add_error(None, ValidationError(u"La contraseña anterior es inválida", code='old_invalid'))
            return self.form_invalid(form)
        else:
            self.request.user.set_password(form.cleaned_data['contrasena_nueva'])
            registrar_cambio_contrasena(self.request.user, None)
            self.request.user.save()
        return super(CambiarContrasenaView, self).form_valid(form)

def cambiar_password_conf(request):
    return render(request, 'FacturasNorte/base/cambiar_contrasena_hecho.html', {})

class ClienteModifView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "FacturasNorte/empleado/mod_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.update_cliente'

class ClienteRegistroView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ClienteLegado
    form_class = ClienteLegadoForm
    template_name = "FacturasNorte/empleado/registro_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.update_cliente'

    def get_object(self, queryset=None):
        object = super(ClienteRegistroView, self).get_object()
        object.nombre = object.nombre.strip()
        object.domicilio = object.domicilio.strip()
        object.nroDoc = object.nroDoc.strip()
        object.telefono = object.telefono.strip()
        object.email = object.email.strip()
        return object

    def form_valid(self, form):
        crear_perfil(form, 'cliente')
        crear_historial_alta(form, self.request.user)
        self.object.fechaUpdate = corregir_fecha_update(self.object)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ClienteDeBajaRegistroView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "FacturasNorte/empleado/registro_cliente.html"
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.update_cliente'

    def form_valid(self, form):
        self.object.set_activo(True)
        crear_historial_alta(form, self.request.user)
        return super(ClienteDeBajaRegistroView, self).form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, LogicDeleteView):
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
    permission_required = 'FacturasNorte.view_lista_cliente'
    form_class = FiltroClienteForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ClienteListView, self).get_initial()
        try:
            initial['query'] = self.request.GET['query']
            initial['tipo'] = self.request.GET['tipo']
            initial['activo'] = self.request.GET['activo']
        finally:
            return initial

    def get_queryset(self):
        try:
            return search_model(Cliente, self.request.GET['tipo'], self.request.GET['query'], self.request.GET['activo'], False)
        except KeyError:
            return Cliente.objects.filter(activo=True)

class ClientesLegadosView(ClienteListView):
    template_name = "FacturasNorte/empleado/clientes_legados.html"
    model = ClienteLegado
    context_object_name = 'cliente_list'
    paginate_by = 10
    permission_required = 'FacturasNorte.view_lista_cliente'
    form_class = FiltroClienteForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ClientesLegadosView, self).get_initial()
        try:
            initial['query'] = self.request.GET['query']
            initial['tipo'] = self.request.GET['tipo']
        finally:
            return initial

    def get_queryset(self):
        try:
            return search_model(ClienteLegado, self.request.GET['tipo'], self.request.GET['query'], False, False )
        except KeyError:
            return ClienteLegado.objects.all()

class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/empleado/cliente_detail.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_detalle_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ClienteFacturasView(LoginRequiredMixin, PermissionRequiredMixin, CustomClienteDetailView, FormMixin):
    template_name = "FacturasNorte/cliente/facturas_list.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_facturas'
    form_class = FiltroFacturaForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ClienteFacturasView, self).get_initial()
        try:
            initial['numero'] = self.request.GET['numero']
            initial['tipo'] = self.request.GET['tipo']
        finally:
            return initial

    def get_context_data(self, **kwargs):
        context = super(ClienteFacturasView, self).get_context_data(**kwargs)
        context['form'] = self.get_form(FiltroFacturaForm)
        try:
            dia = int(self.request.GET['fecha_day'])
            mes = int(self.request.GET['fecha_month'])
            anio = int(self.request.GET['fecha_year'])
            fecha = date(anio, mes, dia)
        except (MultiValueDictKeyError, ValueError):
            fecha = None
        try:
            field = self.request.GET['tipo']
            if field in ('2', '4'):
                context['lista_facturas'] = buscar_pdfs_pedidos(self.kwargs.get(self.pk_url_kwarg),
                                                    field=self.request.GET['tipo'],
                                                    pedido=self.request.GET['numero'],
                                                    fecha_pedido=fecha)
            else:
                 context['lista_facturas'] = buscar_pdfs_facturas(self.kwargs.get(self.pk_url_kwarg),
                                                    field=self.request.GET['tipo'],
                                                    factura=self.request.GET['numero'],
                                                    fecha_factura=fecha)

        except KeyError:
            context['lista_facturas'] = buscar_pdfs_pedidos(self.kwargs.get(self.pk_url_kwarg))
        return context

class EmpleadoListaFacturasView(LoginRequiredMixin, PermissionRequiredMixin, CustomClienteDetailView, FormMixin):
    template_name = "FacturasNorte/empleado/facturas_cliente.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_facturas'
    form_class = FiltroFacturaForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(EmpleadoListaFacturasView, self).get_initial()
        try:
            initial['pedido'] = self.request.GET['pedido']
            initial['tipo'] = self.request.GET['tipo']
            initial['fecha_day'] = self.request.GET['fecha_day']
            initial['fecha_month'] = self.request.GET['fecha_month']
            initial['fecha_year'] = self.request.GET['fecha_year']
        finally:
            return initial

    def get_context_data(self, **kwargs):
        context = super(EmpleadoListaFacturasView, self).get_context_data(**kwargs)
        context['form'] = self.get_form(FiltroFacturaForm)
        try:
            dia = int(self.request.GET['fecha_day'])
            mes = int(self.request.GET['fecha_month'])
            anio = int(self.request.GET['fecha_year'])
            fecha = date(anio, mes, dia)
        except (MultiValueDictKeyError, ValueError):
            fecha = None
        try:
            field = self.request.GET['tipo']
            if field in ('2', '4'):
                context['lista_facturas'] = buscar_pdfs_pedidos(self.kwargs.get(self.pk_url_kwarg),
                                                    field=self.request.GET['tipo'],
                                                    pedido=self.request.GET['numero'],
                                                    fecha_pedido=fecha)
            else:
                 context['lista_facturas'] = buscar_pdfs_facturas(self.kwargs.get(self.pk_url_kwarg),
                                                    field=self.request.GET['tipo'],
                                                    factura=self.request.GET['numero'],
                                                    fecha_factura=fecha)

        except KeyError:
            context['lista_facturas'] = buscar_pdfs_pedidos(self.kwargs.get(self.pk_url_kwarg))
        return context

class ClienteRegenerarContrasenaView(FormView):
    template_name = 'FacturasNorte/base/reset_contrasena_form.html'
    form_class = RegenerarContrasenaForm

    def form_valid(self, form):
        usuario = User.objects.get(email=form.cleaned_data['username'])
        empleado = Empleado.objects.get(nroUsuario=self.request.user.username)
        reset_password(usuario, empleado)
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
        usuario = Cliente.objects.get(id=pk).nroUsuario
    except ObjectDoesNotExist:
        usuario = Empleado.objects.get(id=pk).nroUsuario

    return render(request, 'FacturasNorte/base/reset_contrasena.html', {'usuario':usuario})

class ConfigurationView(FormView):
    template_name = 'FacturasNorte/admin/configuration.html'
    form_class = ConfigurationForm
    success_url = reverse_lazy('FacturasNorte:config_done')

    def form_valid(self, form):
        pdf_root = 'PDF_ROOT = ' + "'" + form.cleaned_data['pdf_root'] + "'"
        email_entrada = 'EMAIL_ENTRADA = ' + "'" + form.cleaned_data['email_entrada'] + "'"
        email_salida = 'EMAIL_SALIDA = ' + "'" +  form.cleaned_data['email_salida'] + "'"
        facturas = "PDF_FACTURAS = PDF_ROOT + 'facturas/' "
        pedidos = "PDF_PEDIDOS = PDF_ROOT + 'pedidos/' "

        f = open('C:\Apache24\htdocs\Norte\FacturasNorte\config.py','w')
        file = File(f)
        file.write(pdf_root)
        file.write('\n')
        file.write(facturas)
        file.write('\n')
        file.write(pedidos)
        file.write('\n')
        file.write(email_entrada)
        file.write('\n')
        file.write(email_salida)
        file.close()
        return render (self.request, 'FacturasNorte/admin/config_success.html')

def configuration_done (request):
    return render (request, 'FacturasNorte/admin/config_success.html')

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
        email = form.cleaned_data.get('username')

        if self.request.user.is_authenticated():
            send_email_contact(self.request.user.email, subject, body)

        else:
            send_email_contact(email, subject, body)
            messages.success(self.request, 'Email enviado con exito')


        return super(ContactView, self).form_valid(form)

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "FacturasNorte/home.html"
    paginate_by = 2

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "FacturasNorte/post.html"


def reestablecer_password(request, pk):
    usuario = get_object_or_404(User, id=pk)
    empleado = get_object_or_404(Empleado, email=request.user.email)
    reset_password(usuario, empleado)
    return render(request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})

class Historial(generic.DetailView):
    model = models.Historiales
    template_name = "FacturasNorte/historial.html"

class Historial_register(generic.DetailView):
    model = models.Historiales_registros
    template_name = "FacturasNorte/historial_register.html"

def pdf_help(request):
    pdf = open_pdf_view(config.PDF_ROOT, "ayuda.pdf")

    return pdf


@login_required
def pdf_view(request, ruta):
    cuit = ruta.split('-')[1]
    if request.user.is_staff or request.user.is_superuser:
        return open_pdf_view(request, ruta)
    else:
        try:
            id = request.user.id
            cliente = Cliente.objects.get(nroUsuario=id)
            if cliente.cuit == cuit:
                return open_pdf_view(request, ruta)
            else:

                return reverse('FacturasNorte:404')
        except ObjectDoesNotExist:
            return reverse('FacturasNorte:404')

            return not_found_view(request)
        except ObjectDoesNotExist:
            return not_found_view(request)


def open_pdf_view(request, ruta):
    ruta = config.PDF_ROOT + ruta
    pdf = open(ruta, 'rb').read()
    response = HttpResponse(pdf, content_type='application/pdf')
    return response

def not_found_view(request):
    response = render_to_response('FacturasNorte/errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def error_view(request):
    response = render_to_response('FacturasNorte/errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def permission_denied_view(request):
    response = render_to_response('FacturasNorte/errors/403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response

def bad_request_view(request):
    response = render_to_response('FacturasNorte/errors/400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response


