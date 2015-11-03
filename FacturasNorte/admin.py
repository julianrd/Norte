from django.contrib.auth.models import Permission

__author__ = 'Julian'
from django.contrib import admin
from FacturasNorte.models import Cliente, Empleado, Entry, Tag, Historiales, HistorialContrasena, Historiales_registros

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

class EmpleadoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nroUsuario', 'nombre', 'email', 'domicilio', 'admin']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'email', 'domicilio', 'telefono', 'admin')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']

class EntryAdmin(MarkdownModelAdmin):
    list_display = ("title", "created")
    prepopulated_fields = {"slug": ("title",)}
    # Next line is a workaround for Python 2.x
    #formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


class HistorialAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'nroUsuario', 'nombre', 'fecha', 'perfil', 'autenticado', 'ip')
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


class HistorialContrasenaAdmin(admin.ModelAdmin):
    readonly_fields = ('nroUsuario', 'nombre', 'email', 'fecha', 'reestablecida_por_empleado', 'nombre_empleado', 'dni_empleado')
    list_display = ('nroUsuario', 'nombre', 'email', 'fecha', 'reestablecida_por_empleado', 'nombre_empleado', 'dni_empleado')
    list_filter = ['reestablecida_por_empleado']
    search_fields = ['nombre', 'email', 'fecha', 'dni_empleado', 'reestablecida_por_empleado']

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Historiales, HistorialAdmin)
admin.site.register(Historiales_registros, HistorialAdminRegister)
admin.site.register(HistorialContrasena, HistorialContrasenaAdmin)




