# -*- coding: utf-8 -*-

import urllib.parse

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from django.utils import timezone
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import generic

from FacturasNorte.custom_classes import CustomClienteDetailView, CustomAdminDetailView, CustomEmpleadoDetailView, \
    LogicDeleteView, FormListView
from FacturasNorte.functions import send_email_contact, reset_password, buscar_pdfs, \
    crear_perfil, search_legado, search_model
from Norte import settings
from . import models


#Importaciones para conficuracion de contacto

from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from FacturasNorte.forms import CambiarContrasenaForm, ContactUsuarioAnonimoForm, ContactUsuarioLoginForm, \
    IniciarSesionForm, RegenerarContrasenaForm, FiltroPersonaForm, FiltroFacturaForm, ClienteForm, \
    EmpleadoForm, ClienteLegadoForm, FiltroClienteForm

from FacturasNorte.forms import  EmpleadoRegisterForm
from FacturasNorte.models import Empleado, Cliente, ClienteLegado
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
        try:
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
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

        redirect_to_string = str(redirect_to)
        netloc = urllib.parse.urlsplit(redirect_to_string)[1]
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

    def get_queryset(self):
        try:
            return search_model(Empleado,self.request.GET['tipo'], self.request.GET['query'], True, True)
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

class EmpCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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
        self.success_url = reverse_lazy('FacturasNorte:perfil_empleado',kwargs={'pk' : self.request.user.id})
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

    def get_queryset(self):
        try:
            return search_model(Empleado, self.request.GET['tipo'], self.request.GET['query'], True, False)
        except KeyError:
            return Empleado.objects.filter(activo=True)

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

class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/empleado/add_cliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.agregar_cliente'

    def form_valid(self, form):
        # if form.non_field_errors():
        #     return reverse('FacturasNorte:nuevo_cliente')
        crear_perfil(form, 'cliente')
        return super(ClienteCreateView, self).form_valid(form)

class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/base/cambiar_contrasena.html"
    form_class = CambiarContrasenaForm
    success_url = reverse_lazy('FacturasNorte:cambiar_contrasena_hecho')
    permission_required = 'FacturasNorte.cambiar_cont'

    def form_valid(self, form):
        if not self.request.user.check_password(form.cleaned_data.get('contrasena_anterior')):
            raise ValidationError(u"La contraseÃ±a anterior es invÃ¡lida", code='old_invalid')
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

    def form_valid(self, form):
        crear_perfil(form, 'cliente')
        return super(ClienteRegistroView, self).form_valid(form)

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

    # def get_initial(self):
    #     """
    #     Returns the initial data to use for forms on this view.
    #     """
    #     initial = super(ClienteListView, self).get_initial()
    #     try:
    #         initial['query'] = self.request.session['query']
    #         initial['tipo'] = self.request.session['tipo']
    #         initial['activo'] = self.request.session['activo']
    #     finally:
    #         return initial
    #
    # def post(self, request, *args, **kwargs):
    #     request.session.__setitem__('query', request.form.cleaned_data['query'])
    #     request.session.__setitem__('tipo', request.form.cleaned_data['tipo'])
    #     request.session.__setitem__('activo', request.form.cleaned_data['activo'])
    #     return self.get(request, *args, **kwargs)

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

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form(FiltroFacturaForm)
    #     URL = 'FacturasNorte/cliente/facturas/' + self.kwargs.get(self.pk_url_kwarg) + '/'
    #     if form.is_valid():
    #         if (form.cleaned_data['tipo'] == 'fecha'):
    #             fecha = form.cleaned_data['fecha'].strftime("%Y-%m-%d")
    #             return search_redirect(URL, form.cleaned_data['tipo'], fecha)
    #         elif (form.cleaned_data['tipo'] == 'pedido'):
    #             return search_redirect(URL, form.cleaned_data['tipo'], form.cleaned_data['pedido'])
    #         else:
    #             return redirect(URL)
    #     else:
    #         return redirect('/' + URL)

    def get_context_data(self, **kwargs):
        context = super(ClienteFacturasView, self).get_context_data(**kwargs)
        context['form'] = self.get_form(FiltroFacturaForm)
        try:
            context['lista_facturas'] = buscar_pdfs(self.kwargs.get(self.pk_url_kwarg),
                                                    self.request.GET['tipo'],
                                                    self.request.GET['query'])
        except KeyError:
            context['lista_facturas'] = buscar_pdfs(self.kwargs.get(self.pk_url_kwarg))
        return context

class EmpleadoListaFacturasView(ClienteFacturasView):
    template_name = "FacturasNorte/empleado/facturas_cliente.html"
    permission_required = 'FacturasNorte.view_facturas'

    def get_context_data(self, **kwargs):
        context = super(EmpleadoListaFacturasView, self).get_context_data(**kwargs)
        context['form'] = self.get_form(FiltroFacturaForm)
        try:
            context['lista_facturas'] = buscar_pdfs(self.kwargs.get(self.pk_url_kwarg),
                                                    self.kwargs['tipo'],
                                                    self.kwargs['query'])
        except KeyError:
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
        usuario = get_object_or_404(Cliente, id=pk).nroUsuario
    except ObjectDoesNotExist:
        usuario = get_object_or_404(Empleado, id=pk).nroUsuario

    return render(request, 'FacturasNorte/base/reset_contrasena.html', {'usuario':usuario})

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

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "FacturasNorte/home.html"
    paginate_by = 2

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "FacturasNorte/post.html"



def reestablecer_password(request, pk):
    usuario = get_object_or_404(User, id=pk)
    reset_password(usuario)
    return render(request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})

