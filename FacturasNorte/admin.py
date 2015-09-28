from django.contrib.auth.models import Permission

__author__ = 'Julian'
from django.contrib import admin
from FacturasNorte.models import Cliente, Empleado, Entry, Tag

from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

# Register your models here.
class PermissionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'codename']})]
    list_display = ('name', 'codename')
    list_filter = ['name']
    search_fields = ['codename']

class ClienteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nroUsuario', 'nombre', 'email', 'domicilio', 'cuit', 'activo']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']

class AdministradorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nroUsuario', 'nombre', 'dni', 'email', 'domicilio', 'telefono']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'dni', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']


class EmpleadoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nroUsuario', 'nombre', 'email', 'domicilio']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']

class EntryAdmin(MarkdownModelAdmin):
    list_display = ("title", "created")
    prepopulated_fields = {"slug": ("title",)}
    # Next line is a workaround for Python 2.x
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)



