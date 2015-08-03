__author__ = 'Julian'
from django.contrib import admin
from FacturasNorte.models import Cliente, Administrador, Empleado

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'email', 'domicilio']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']

class AdministradorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'dni', 'email', 'domicilio', 'telefono']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'dni', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']


class EmpleadoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'email', 'domicilio']}),
        ('Date information', {'fields':['fechaNacimiento'], 'classes':['collapse']}),
    ]
    list_display = ('nombre', 'fechaNacimiento', 'email', 'domicilio', 'telefono')
    list_filter = ['fechaNacimiento']
    search_fields = ['nombre']

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Empleado, AdministradorAdmin)


