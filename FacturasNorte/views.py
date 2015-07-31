__author__ = 'Julian'
from django.contrib.auth import views
from django.utils import timezone
from FacturasNorte.forms import AdminRegisterForm, ClienteRegisterForm
from FacturasNorte.models import Administrador, Cliente
from FacturasNorte.models import User
from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class AdminCreateView(FormView):
    template_name = "FacturasNorte/admin/add_admin.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_admin')

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

class ClienteCreateView(FormView):
    template_name = "FacturasNorte/staff/add_cliente.html"
    form_class = ClienteRegisterForm
    success_url = reverse_lazy('FacturasNorte:lista_cliente')

    def form_valid(self, form):

        #Nuevo Usuario
        nuevo_usuario = User()
        nuevo_usuario.username = form.cleaned_data['email_field'].split("@")[0]
        nuevo_usuario.set_password(form.cleaned_data['password_field'])
        nuevo_usuario.email = form.cleaned_data['email_field']
        nuevo_usuario.is_active = True
        nuevo_usuario.is_staff = False
        nuevo_usuario.is_superuser = False
        nuevo_usuario.date_joined = timezone.now()
        nuevo_usuario.save()

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
    if request.user.is_staff:
        return render(request, 'FacturasNorte/empleado/index.html')
    elif request.user.is_authenticated():
        return render(request, 'FacturasNorte/cliente/index.html')
    else:
        return render(request, 'FacturasNorte/registration/login_required.html')
