from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from Norte import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Norte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^FacturasNorte/', include('FacturasNorte.urls', namespace='FacturasNorte')),
)