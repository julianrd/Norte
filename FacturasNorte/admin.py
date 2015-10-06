from django.contrib.auth.models import Permission

__author__ = 'Julian'
from django.contrib import admin
from FacturasNorte.models import Cliente, Empleado, Entry, Tag, Historiales, Historiales_registros

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

class HistorialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nroUsuario', 'nombre', 'fecha', 'perfil', 'autenticado', 'ip']}),
        ('Date information', {'fields':['nroUsuario','nombre'], 'classes':['collapse']}),
    ]
    list_display = ('id', 'nroUsuario', 'nombre', 'fecha', 'perfil', 'autenticado', 'ip')
    list_filter = ['autenticado']
    search_fields = ['nombre', 'id', 'nroUsuario', 'nombre', 'fecha', 'perfil', 'autenticado', 'ip']

class HistorialAdminRegister(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['cuit_cli', 'nombre', 'fecha', 'operador', 'accion']}),
        ('Date information', {'fields':['id','cuit_cli'], 'classes':['collapse']}),
    ]
    list_display = ('id', 'cuit_cli', 'nombre', 'fecha', 'operador', 'accion')
    list_filter = ['cuit_cli']
    search_fields = ['cuit_cli', 'nombre', 'fecha', 'operador', 'accion']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Historiales, HistorialAdmin)
admin.site.register(Historiales_registros, HistorialAdminRegister)



