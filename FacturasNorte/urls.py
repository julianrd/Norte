__author__ = 'Julian'
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views, feed

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^superadmin/', include(admin.site.urls)),

    url(r'^login/$', auth_views.login, {'template_name': 'FacturasNorte/registration/login.html'}, name='login'),
    url(r'^admin/$', views.index, name = 'index'),
    url(r'^empleado/$', views.index, name = 'index'),
    url(r'^cliente/$', views.index, name = 'index'),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'FacturasNorte/registration/logged_out.html'}, name='logout'),

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

    url(r'^staff/nuevo_cliente/$', views.ClienteCreateView.as_view(), name = 'nuevo_cliente'),
    url(r'^staff/cliente/(?P<pk>\d+)/$', views. ClienteDetailView.as_view(), name = 'detalle_cliente'),
    url(r'^staff/lista_cliente/$', views.ClienteListView.as_view(), name = 'lista_cliente'),
    url(r'^staff/del_cliente/(?P<pk>\d+)/$', views.ClienteDeleteView.as_view(), name = 'elim_cliente'),
    url(r'^staff/mod_cliente/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'modif_cliente'),



    url(r'contact/$', views.ContactView.as_view(), name = 'contacto'),
    url(r'thankyou/$', views.ThankYou, name ='thankyou'),



    url(r'^staff/nuevo_empleado/$', views.EmpCreateView.as_view(), name = 'nuevo_empleado'),
    url(r'^staff/empleado/(?P<pk>\d+)/$', views.EmpDetailView.as_view(), name = 'detalle_empleado'),
    url(r'^staff/lista_empleado/$', views.EmpListView.as_view(), name = 'lista_empleado'),
    url(r'^staff/del_empleado/(?P<pk>\d+)/$', views.EmpDeleteView.as_view(), name = 'elim_empleado'),
    url(r'^staff/mod_empleado/(?P<pk>\d+)/$', views.EmpModifView.as_view(), name = 'modif_empleado'),

    url(r'^cliente/reset_pass/$', views.reset_password_conf, name = 'regenerar_contrasena?'),
    url(r'^cliente/reset_pass/conf/$', views.reset_password, name = 'regenerar_contrasena_hecho'),
    url(r'^cliente/factura/$', views.pdf_view, name = 'factura'),

    url(r'contact/$', views.ContactView.as_view(), name = 'contacto'),

    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^home/$', views.BlogIndex.as_view(), name="index"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),


)