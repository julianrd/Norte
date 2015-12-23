from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.views.generic import DeleteView, ListView

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from FacturasNorte.functions import crear_historial_baja
from FacturasNorte.models import Empleado, Cliente

__author__ = 'Julian'

class CustomAdminDetailView(DetailView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = Empleado.objects.filter(admin=True)

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(nroUsuario=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class CustomEmpleadoDetailView(DetailView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = Empleado.objects

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(nroUsuario=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class CustomClienteDetailView(DetailView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = Cliente.objects

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(nroUsuario=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class Pagina(object):
    ruta = None

    def get_ruta(self):
        return self.ruta

    def set_ruta(self, ruta):
        self.ruta = ruta
        return

class Factura(object):
    cliente = None
    fechaPed = None
    fechaFac = None
    nroPedido = None
    nroFactura = None
    rutaPed = None
    rutaFac = None

    def get_nroFactura(self):
        return self.nroFactura

    def set_nroFactura(self, nroFactura):
        self.nroFactura = nroFactura
        return

    def get_nroPedido(self):
        return self.nroPedido

    def set_nroPedido(self, nroPedido):
        self.nroPedido = nroPedido
        return

    def get_cliente(self):
        return self.cliente

    def get_fechaPed(self):
        return self.fechaPed

    def get_fechaFac(self):
        return self.fechaFac

    def set_cliente(self, cliente):
        self.cliente = cliente
        return

    def set_fechaPed(self, fecha):
        self.fechaPed = fecha
        return

    def set_fechaFac(self, fecha):
        self.fechaFac = fecha
        return

    def set_rutaPed(self, ruta):
        self.rutaPed = ruta
        return

    def set_rutaFac(self, ruta):
        self.rutaFac = ruta
        return

    def get_rutaPed(self):
        return self.rutaPed

    def get_rutaFac(self):
        return self.rutaFac

class LogicDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.set_activo(False)
        self.object.nroUsuario.is_active = False
        try:
            crear_historial_baja(self.request.user, self.object)
            self.object.save()
            self.object.nroUsuario.save()
        finally:
            return HttpResponseRedirect(success_url)

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

class Diario(object):
    fecha = None
    ruta = None

    def set_fecha(self, fecha):
        self.fecha = fecha
        return

    def get_fecha(self):
        return self.fecha

    def set_ruta(self, ruta):
        self.ruta = ruta
        return

    def get_ruta(self):
        return self.ruta

