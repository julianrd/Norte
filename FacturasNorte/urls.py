import FacturasNorte
from FacturasNorte.views import ClienteListView
from FacturasNorte import config

__author__ = 'Julian'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views, feed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^superadmin/', include(admin.site.urls)),
    url(r'^$', views.BlogIndex.as_view(), name = 'index'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cambiar_pass/$', views.CambiarContrasenaView.as_view(), name = 'cambiar_contrasena'),
    url(r'^cambiar_pass/conf/$', views.cambiar_password_conf, name = 'cambiar_contrasena_hecho'),
    url(r'^reset_pass/$', views.ClienteRegenerarContrasenaView.as_view(), name = 'reestablecer_contrasena_form'),
    url(r'^reset_user_pass/(?P<pk>\d+)/$', views.reset_password_conf, name = 'reestablecer_contrasena'),
    url(r'^reset_pass/conf/(?P<pk>\d+)/$', views.reestablecer_password, name = 'reestablecer_contrasena_hecho'),
    url(r'^contacto/$', views.ContactView.as_view(), name = 'contacto'),
    url(r'^thankyou/$', views.thank_you, name ='thankyou'),
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),
    url(r'^historiales/(?P<slug>\S+)$', views.Historial.as_view(), name="historial"),
    url(r'^historial_register/(?P<pk>\d+)/$', views.HistorialRegister.as_view(), name = 'historial_register'),

    url(r'^admin/perfil/(?P<pk>\d+)/$', views. AdminPerfilView.as_view(), name = 'perfil_admin'),
    url(r'^admin/nuevo_admin/$', views.AdminCreateView.as_view(), name = 'nuevo_admin'),
    url(r'^admin/(?P<pk>\d+)/$', views. AdminDetailView.as_view(), name = 'detalle_admin'),
    url(r'^admin/admins/$', views.AdminListView.as_view(), name = 'lista_admin'),
    url(r'^admin/del_admin/(?P<pk>\d+)/$', views.delete_admin_view, name = 'elim_admin'),
    url(r'^admin/mod_admin/(?P<pk>\d+)/$', views.EmpModifPerfilView.as_view(), name = 'modif_admin'),
    url(r'^admin/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^admin/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^admin/empleados/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^admin/del_empleado/(?P<pk>\d+)/$', views.delete_emp_view, name = 'elim_empleado'),
    url(r'^admin/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),
    url(r'^admin/config/$', views.ConfigurationView.as_view(), name = 'config'),
    url(r'^admin/config/$', views.configuration_done, name = 'config_done'),

    url(r'^staff/perfil/(?P<pk>\d+)/$', views. EmpleadoPerfilView.as_view(), name = 'perfil_empleado'),
    #url(r'^staff/nuevo_cliente/$', views.ClienteCreateView.as_view(), name = 'nuevo_cliente'),
    url(r'^staff/registro_cliente/$', views.ClientesLegadosView.as_view(), name = 'clientes_legados'),
    url(r'^staff/registro_cliente/(?P<pk>\d+)/$', views.ClienteRegistroView.as_view(), name = 'registro_cliente'),
    url(r'^staff/registro_cliente_baja/(?P<pk>\d+)/$', views.ClienteDeBajaRegistroView.as_view(), name = 'registro_cliente_de_baja'),
    url(r'^staff/cliente/(?P<pk>\d+)/$', views. ClienteDetailView.as_view(), name = 'detalle_cliente'),
    url(r'^staff/clientes/$', views.ClienteListView.as_view(), name = 'lista_cliente'),
    url(r'^staff/del_cliente/(?P<pk>\d+)/$', views.delete_cliente_view, name = 'elim_cliente'),
    url(r'^staff/mod_cliente/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'modif_cliente'),
    url(r'^staff/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^staff/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^staff/empleados/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^staff/del_empleado/(?P<pk>\d+)/$', views.delete_emp_view, name = 'elim_empleado'),
    url(r'^staff/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),
    url(r'^staff/mod_perfil/(?P<pk>\d+)/$', views.EmpModifPerfilView.as_view(), name = 'modif_perfil'),
    url(r'^staff/facturas/(?P<pk>\d+)/$', views.EmpleadoListaFacturasView.as_view(), name = 'facturas_cliente_empleado'),

    # url(r'^cliente/edit/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'edit_cliente'),
    url(r'^cliente/perfil/(?P<pk>\d+)/$', views.ClientePerfilView.as_view(), name = 'perfil_cliente'),
    url(r'^cliente/facturas/(?P<pk>\d+)/$', views.ClienteFacturasView.as_view(), name = 'facturas_cliente'),
    url(r'^factura/(?P<ruta>.*)$', views.pdf_factura_view, name = 'ver_factura'),
    url(r'^pedido/(?P<ruta>.*)$', views.pdf_pedido_view, name = 'ver_pedido'),
    url(r'^diario/$', views.pdf_diario_view, name = 'diario_hoy'),
    url(r'^diarios/$', views.ListaDiariosView.as_view(), name = 'lista_diarios'),
    url(r'^pdf_ayuda/$', views.pdf_help, name = 'ver_ayuda'),
    url(r'^pdf_diario/(?P<ruta>.*)$', views.pdf_diario, name = 'ver_diario'),
    url(r'^open_diario/(?P<ruta>.*)$', views.open_diario.as_view(), name = 'open_diario'),




    url(r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {'document_root': config.PDF_ROOT}, name = 'media'),


)

# static files (images, css, javascript, etc.)
urlpatterns += patterns('',
    (r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': config.PDF_ROOT}))

urlpatterns += staticfiles_urlpatterns()

#error pages

handler404 = 'FacturasNorte.views.not_found_view'

handler500 = 'FacturasNorte.views.error_view'

handler403 = 'FacturasNorte.views.permission_denied_view'

handler400 = 'FacturasNorte.views.bad_request_view'
