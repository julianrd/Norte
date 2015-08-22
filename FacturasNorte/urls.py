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
    url(r'^$', views.index, name = 'index'),
    url(r'^base/$', views.base, name = 'index'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cambiar_pass/$', views.ClienteCambiarContrasenaView.as_view(), name = 'cambiar_contrasena'),
    url(r'^cambiar_pass/conf/$', views.cambiar_password_conf, name = 'cambiar_contrasena_hecho'),
    url(r'^contacto/$', views.ContactView.as_view(), name = 'contacto'),
    url(r'^thankyou/$', views.ThankYou, name ='thankyou'),

    url(r'^admin/perfil/(?P<pk>\d+)/$', views. AdminPerfilView.as_view(), name = 'perfil_admin'),
    url(r'^admin/nuevo_admin/$', views.AdminCreateView.as_view(), name = 'nuevo_admin'),
    url(r'^admin/(?P<pk>\d+)/$', views. AdminDetailView.as_view(), name = 'detalle_admin'),
    url(r'^admin/lista_admin/$', views.AdminListView.as_view(), name = 'lista_admin'),
    url(r'^admin/del_admin/(?P<pk>\d+)/$', views.AdminDeleteView.as_view(), name = 'elim_admin'),
    url(r'^admin/mod_admin/(?P<pk>\d+)/$', views.AdminModifView.as_view(), name = 'modif_admin'),
    url(r'^admin/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^admin/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^admin/lista_empleado/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^admin/del_empleado/(?P<pk>\d+)/$', views.EmpDeleteView.as_view(), name = 'elim_empleado'),
    url(r'^admin/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),

    url(r'^staff/perfil/(?P<pk>\d+)/$', views. EmpleadoPerfilView.as_view(), name = 'perfil_empleado'),
    url(r'^staff/nuevo_cliente/$', views.ClienteCreateView.as_view(), name = 'nuevo_cliente'),
    url(r'^staff/cliente/(?P<pk>\d+)/$', views. ClienteDetailView.as_view(), name = 'detalle_cliente'),
    url(r'^staff/lista_cliente/$', views.ClienteListView.as_view(), name = 'lista_cliente'),
    url(r'^staff/del_cliente/(?P<pk>\d+)/$', views.ClienteDeleteView.as_view(), name = 'elim_cliente'),
    url(r'^staff/mod_cliente/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'modif_cliente'),
    url(r'^staff/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^staff/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^staff/lista_empleado/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^staff/del_empleado/(?P<pk>\d+)/$', views.EmpDeleteView.as_view(), name = 'elim_empleado'),
    url(r'^staff/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),

    url(r'^cliente/perfil/(?P<pk>\d+)/$', views.ClientePerfilView.as_view(), name = 'perfil_cliente'),
    url(r'^cliente/reset_pass/$', views.ClienteRegenerarContrasenaView.as_view(), name = 'regenerar_contrasena_form'),
    url(r'^cliente/reset_pass/(?P<pk>\d+)/$', views.reset_password_conf, name = 'regenerar_contrasena?'),
    url(r'^cliente/reset_pass/(?P<pk>\d+)/conf/$', views.reset_password, name = 'regenerar_contrasena_hecho'),
    url(r'^cliente/factura/$', views.pdf_view, name = 'factura'),
    url(r'^cliente/facturas/(?P<pk>\d+)/$', views.ClienteFacturasView.as_view(), name = 'facturas_cliente'),


    url(r'contact/$', views.ContactView.as_view(), name = 'contacto'),
    url(r'thankyou/$', views.ThankYou, name ='thankyou'),
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^home/$', views.BlogIndex.as_view(), name="home"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),

    url(r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name = 'media')
)

# static files (images, css, javascript, etc.)
urlpatterns += patterns('',
    (r'^pdf/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))

urlpatterns += staticfiles_urlpatterns()