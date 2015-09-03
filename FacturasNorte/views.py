import urlparse

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from FacturasNorte.custom_classes import CustomClienteDetailView, CustomAdminDetailView, CustomEmpleadoDetailView
from FacturasNorte.functions import send_email_contact, reset_password, buscar_pdfs, search_redirect, search_person, \
    crear_perfil

__author__ = 'Julian'
from django.utils import timezone
from django import forms

from Norte import settings

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import login, logout, authenticate

from django.views import generic
from . import models

#Importaciones para conficuracion de contacto

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages

from FacturasNorte.forms import CambiarContrasenaForm, ContactUsuarioAnonimoForm, ContactUsuarioLoginForm, \
    IniciarSesionForm, RegenerarContrasenaForm, FiltroPersonaForm, FiltroFacturaForm

from FacturasNorte.forms import AdminRegisterForm, EmpleadoRegisterForm, ClienteRegisterForm

from FacturasNorte.models import Administrador, Empleado, Cliente
from FacturasNorte.models import User

#Pruebas de Usuario
def is_admin_o_emp(user):
    return user.is_superuser or user.is_staff

class FormListView(FormMixin, ListView):
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
        try:
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(self.request, user)
        except Exception:
            form.add_error('password', ValidationError('Contrasena incorrecta', code='authentication'))
            return self.form_invalid(form)
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
        try:
            crear_perfil(form, Administrador)
            return super(AdminCreateView, self).form_valid(form)
        except ValidationError:
            return render(self.request, 'FacturasNorte/admin/add_admin_error.html')

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

    form_class = FiltroPersonaForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(FiltroPersonaForm)
        if form.is_valid():
            URL = 'FacturasNorte/admin/admins/'
            return search_redirect(URL, form.cleaned_data['tipo'], form.cleaned_data['query'])

    def get_queryset(self):
        try:
            return search_person(Administrador, self.kwargs['tipo'], self.kwargs['query'])
        except KeyError:
            return Administrador.objects.all()

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
    permission_required = 'FacturasNorte.view_perfil_empleado'

class EmpCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/admin/add_emp.html"
    form_class = EmpleadoRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_empleado')
    permission_required = 'FacturasNorte.add_empleado'

    def form_valid(self, form):
        try:
            crear_perfil(form, Empleado)
            return super(EmpCreateView, self).form_valid(form)
        except ValidationError:
            return render(self.request, 'FacturasNorte/admin/add_empleado_error.html')

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

    form_class = FiltroPersonaForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(FiltroPersonaForm)
        if form.is_valid():
            URL = 'FacturasNorte/admin/empleados/'
            return search_redirect(URL, form.cleaned_data['tipo'], form.cleaned_data['query'])

    def get_queryset(self):
        try:
            return search_person(Empleado, self.kwargs['tipo'], self.kwargs['query'])
        except KeyError:
            return Empleado.objects.all()

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
    form_class = ClienteRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_cliente')
    permission_required = 'FacturasNorte.agregar_cliente'

    def form_valid(self, form):
        if form.non_field_errors():
            return reverse('FacturasNorte:nuevo_cliente')
        try:
            crear_perfil(form, Cliente)
            return super(ClienteCreateView, self).form_valid(form)
        except ValidationError:
            return render(self.request, 'FacturasNorte/empleado/add_cliente_error.html')

class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "FacturasNorte/base/cambiar_contrasena.html"
    form_class = CambiarContrasenaForm
    success_url = reverse_lazy('FacturasNorte:cambiar_contrasena_hecho')
    permission_required = 'FacturasNorte.cambiar_cont'

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
    permission_required = 'FacturasNorte.update_cliente'

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
    permission_required = 'FacturasNorte.view_lista_cliente'

    form_class = FiltroPersonaForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(FiltroPersonaForm)
        if form.is_valid():
            URL = 'FacturasNorte/staff/clientes/'
            return search_redirect(URL, form.cleaned_data['tipo'], form.cleaned_data['query'])

    def get_queryset(self):
        try:
            return search_person(Cliente, self.kwargs['tipo'], self.kwargs['query'])
        except KeyError:
            return Cliente.objects.all()


class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "FacturasNorte/empleado/cliente_detail.html"
    model = Cliente
    context_object_name = 'cliente'
    permission_required = 'FacturasNorte.view_cliente'

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

    def post(self, request, *args, **kwargs):
        form = self.get_form(FiltroFacturaForm)
        URL = 'FacturasNorte/cliente/facturas/' + self.kwargs.get(self.pk_url_kwarg) + '/'
        if form.is_valid():
            if (form.cleaned_data['tipo'] == 'fecha'):
                fecha = form.cleaned_data['fecha'].strftime("%Y-%m-%d")
                return search_redirect(URL, form.cleaned_data['tipo'], fecha)
            elif (form.cleaned_data['tipo'] == 'pedido'):
                return search_redirect(URL, form.cleaned_data['tipo'], form.cleaned_data['pedido'])
            else:
                return redirect(URL)
        else:
            return redirect('/' + URL)

    def get_context_data(self, **kwargs):
        context = super(ClienteFacturasView, self).get_context_data(**kwargs)
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
        usuario = get_object_or_404(Cliente, numero=pk).nroUsuario
    except ObjectDoesNotExist:
        try:
            usuario = get_object_or_404(Empleado, id=pk).nroUsuario
        except ObjectDoesNotExist:
            usuario = get_object_or_404(Administrador, id=pk).nroUsuario

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

def pdf_view(request):
    with open('C:\Users\Julian\Documents\Diario Norte\Proyecto Norte\PDFs\Hola.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed

def reestablecer_password(request, pk):
    usuario = get_object_or_404(User, id=pk)
    reset_password(usuario)
    return render(request, 'FacturasNorte/base/reset_contrasena_hecho.html', {})