from FacturasNorte.views import ClienteListView
from Norte import settings

__author__ = 'Julian'
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views, feed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^superadmin/', include(admin.site.urls)),
    url(r'^base/$', views.base, name = 'index'),
                       url(r'^$', views.index, name = 'index'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cambiar_pass/$', views.CambiarContrasenaView.as_view(), name = 'cambiar_contrasena'),
    url(r'^cambiar_pass/conf/$', views.cambiar_password_conf, name = 'cambiar_contrasena_hecho'),
    url(r'^reset_pass/$', views.ClienteRegenerarContrasenaView.as_view(), name = 'reestablecer_contrasena_form'),
    url(r'^reset_user_pass/(?P<pk>\d+)/$', views.reset_password_conf, name = 'reestablecer_contrasena'),
    url(r'^reset_pass/conf/(?P<pk>\d+)/$', views.reestablecer_password, name = 'reestablecer_contrasena_hecho'),
    url(r'^contacto/$', views.ContactView.as_view(), name = 'contacto'),
    url(r'^thankyou/$', views.ThankYou, name ='thankyou'),
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^home/$', views.BlogIndex.as_view(), name="home"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),

    url(r'^admin/perfil/(?P<pk>\d+)/$', views. AdminPerfilView.as_view(), name = 'perfil_admin'),
    url(r'^admin/nuevo_admin/$', views.AdminCreateView.as_view(), name = 'nuevo_admin'),
    url(r'^admin/(?P<pk>\d+)/$', views. AdminDetailView.as_view(), name = 'detalle_admin'),
    url(r'^admin/admins/$', views.AdminListView.as_view(), name = 'lista_admin'),
    url(r'^admin/del_admin/(?P<pk>\d+)/$', views.AdminDeleteView.as_view(), name = 'elim_admin'),
    url(r'^admin/mod_admin/(?P<pk>\d+)/$', views.AdminModifView.as_view(), name = 'modif_admin'),
    url(r'^admin/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^admin/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^admin/empleados/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^admin/del_empleado/(?P<pk>\d+)/$', views.EmpDeleteView.as_view(), name = 'elim_empleado'),
    url(r'^admin/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),

    url(r'^staff/perfil/(?P<pk>\d+)/$', views. EmpleadoPerfilView.as_view(), name = 'perfil_empleado'),
    url(r'^staff/nuevo_cliente/$', views.ClienteCreateView.as_view(), name = 'nuevo_cliente'),
    url(r'^staff/alta_cliente/$', views.ClientesLegadosView.as_view(), name = 'clientes_legados'),
    url(r'^staff/alta_cliente/(?P<pk>\d+)/$', views.ClienteRegistroView.as_view(), name = 'registro_cliente'),
    url(r'^staff/cliente/(?P<pk>\d+)/$', views. ClienteDetailView.as_view(), name = 'detalle_cliente'),
    url(r'^staff/clientes/$', views.ClienteListView.as_view(), name = 'lista_cliente'),
    url(r'^staff/del_cliente/(?P<pk>\d+)/$', views.ClienteDeleteView.as_view(), name = 'elim_cliente'),
    url(r'^staff/mod_cliente/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'modif_cliente'),
    url(r'^staff/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^staff/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^staff/empleados/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^staff/del_empleado/(?P<pk>\d+)/$', views.EmpDeleteView.as_view(), name = 'elim_empleado'),
    url(r'^staff/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),
    url(r'^staff/mod_perfil/(?P<pk>\d+)/$', views.EmpModifPerfilView.as_view(), name = 'modif_perfil'),
    url(r'^staff/facturas/(?P<pk>\d+)/$', views.EmpleadoListaFacturasView.as_view(), name = 'facturas_cliente_empleado'),

    url(r'^cliente/perfil/(?P<pk>\d+)/$', views.ClientePerfilView.as_view(), name = 'perfil_cliente'),
    url(r'^cliente/factura/$', views.pdf_view, name = 'factura'),
    url(r'^cliente/facturas/(?P<pk>\d+)/$', views.ClienteFacturasView.as_view(), name = 'facturas_cliente'),


    url(r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name = 'media'),

    url('^cliente/facturas/(?P<pk>\d+)/(?P<tipo>.+)=(?P<query>.+)/$', views.ClienteFacturasView.as_view(), name = 'facturas_search'),
    url('^cliente/facturas/(?P<pk>\d+)/(?P<tipo>.+)=/$', views.ClienteFacturasView.as_view(), name = 'facturas_search'),
    url('^staff/facturas/(?P<pk>\d+)/(?P<tipo>.+)=(?P<query>.+)/$', views.EmpleadoListaFacturasView.as_view(), name = 'facturas_search'),
    url('^staff/facturas/(?P<pk>\d+)/(?P<tipo>.+)=/$', views.EmpleadoListaFacturasView.as_view(), name = 'facturas_search'),
    url('^staff/clientes/(?P<tipo>.+)=(?P<query>.+)/$', views.ClienteListView.as_view(), name = 'clientes_search'),
    url('^staff/clientes/(?P<tipo>.+)=/$', views.ClienteListView.as_view(), name = 'clientes_search'),
    url('^staff/clientes_legados/(?P<tipo>.+)=(?P<query>.+)/$', views.ClientesLegadosView.as_view(), name = 'clientes_search'),
    url('^staff/clientes_legados/(?P<tipo>.+)=/$', views.ClientesLegadosView.as_view(), name = 'clientes_search'),
    url('^admin/empleados/(?P<tipo>.+)=(?P<query>.+)/$', views.EmpListView.as_view(), name = 'empleados_search'),
    url('^admin/empleados/(?P<tipo>.+)=/$', views.EmpListView.as_view(), name = 'empleados_search'),
    url('^admin/admins/(?P<tipo>.+)=(?P<query>.+)/$', views.AdminListView.as_view(), name = 'admins_search'),
    url('^admin/admins/(?P<tipo>.+)=/$', views.AdminListView.as_view(), name = 'admins_search'),
)

# static files (images, css, javascript, etc.)
urlpatterns += patterns('',
    (r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))

urlpatterns += staticfiles_urlpatterns()