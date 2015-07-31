__author__ = 'Julian'
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/nuevo_admin/$', views.AdminCreateView.as_view(), name = 'nuevo_admin'),
    # url(r'^admin/(?P<pk>\d+)/$', views. AdminDetailView.as_view(), name = 'detalle_admin'),
    # url(r'^admin/lista_admin/$', views.AdminListView.as_view(), name = 'lista_admin'),
    # url(r'^admin/del_admin/(?P<pk>\d+)/$', views.AdminDeleteView.as_view(), name = 'elim_admin'),
    # url(r'^admin/mod_admin/(?P<pk>\d+)/$', views.AdminModifView.as_view(), name = 'modif_admin'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', auth_views.login, {'template_name': 'FacturasNorte/registration/login.html'}, name='login'),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'FacturasNorte/registration/logged_out.html'}, name='logout'),

    url(r'^staff/nuevo_cliente/$', views.ClienteCreateView.as_view(), name = 'nuevo_cliente'),
    url(r'^staff/cliente/(?P<pk>\d+)/$', views. ClienteDetailView.as_view(), name = 'detalle_cliente'),
    url(r'^staff/lista_cliente/$', views.ClienteListView.as_view(), name = 'lista_cliente'),
    url(r'^staff/del_cliente/(?P<pk>\d+)/$', views.ClienteDeleteView.as_view(), name = 'elim_cliente'),
    url(r'^staff/mod_cliente/(?P<pk>\d+)/$', views.ClienteModifView.as_view(), name = 'modif_cliente'),


)