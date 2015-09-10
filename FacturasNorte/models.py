__author__ = 'Julian'
from django.db import models
from django.contrib.auth.models import User, Permission, AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.urlresolvers import reverse

class ClienteLegado(models.Model):
    numero = models.AutoField(db_column='NUMERO', primary_key=True)
    nombre = models.CharField(db_column='NOMBRE', max_length=254, blank=True, null=False)  # Field name made lowercase.
    domicilio = models.CharField(db_column='DOMICILIO', max_length=254, blank=True,
                                 null=False)  # Field name made lowercase.
    localidad = models.CharField(db_column='LOCALIDAD', max_length=11, blank=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=254, blank=True,
                                null=False)  # Field name made lowercase.
    condIva = models.CharField(db_column='COND_IVA', max_length=18, blank=True)  # Field name made lowercase.
    email = models.EmailField(db_column='E_MAIL', blank=True, null=True, unique=True)  # Field name made lowercase.
    tipoDoc = models.CharField(db_column='TIPO_DOC', max_length=4, blank=True)  # Field name made lowercase.
    nroDoc = models.CharField(db_column='NRO_DOC', max_length=13, blank=True)  # Field name made lowercase.
    fechaVtoCuit = models.DateTimeField(db_column='FECHAVTOCUIT', blank=True, null=True)  # Field name made lowercase.
    saldo = models.FloatField(db_column='SALDO', blank=True, null=True)  # Field name made lowercase.
    limiteCredito = models.FloatField(db_column='LIMITE_CREDITO', blank=True, null=True)  # Field name made lowercase.
    interesCredito = models.FloatField(db_column='INTERES_CREDITO', blank=True, null=True)  # Field name made lowercase.
    nroCuenta = models.CharField(db_column='NROCUENTA', max_length=20, blank=True)  # Field name made lowercase.
    bonificacion = models.FloatField(db_column='BONIFICACION', blank=True, null=True)  # Field name made lowercase.
    actividad = models.CharField(db_column='ACTIVIDAD', max_length=20, blank=True)  # Field name made lowercase.
    listaPrecio = models.CharField(db_column='LISTA_DE_PRECIO', max_length=9, blank=True)  # Field name made lowercase.
    compctacte = models.CharField(db_column='COMPCTACTE', max_length=20, blank=True)  # Field name made lowercase.
    formaPagoAsociada = models.SmallIntegerField(db_column='FORMAPAGOASOCIADA', blank=True,
                                                 null=True)  # Field name made lowercase.
    aplicarRecargo = models.CharField(db_column='APLICAR_RECARGO', max_length=1,
                                      blank=True)  # Field name made lowercase.
    fechaAlta = models.DateTimeField(db_column='FECHAALTA', blank=True, null=True)  # Field name made lowercase.
    idCodigoContable = models.FloatField(db_column='IDCODIGOCONTABLE', blank=True,
                                         null=True)  # Field name made lowercase.
    telefonoRefencia = models.CharField(db_column='TELEFONOREFENCIA', max_length=20,
                                        blank=True)  # Field name made lowercase.
    lugarTrabajo = models.CharField(db_column='LUGARTRABAJO', max_length=30, blank=True)  # Field name made lowercase.
    domicilioLaboral = models.CharField(db_column='DOMICILIOLABORAL', max_length=30,
                                        blank=True)  # Field name made lowercase.
    telefonoLaboral = models.CharField(db_column='TELEFONOLABORAL', max_length=30,
                                       blank=True)  # Field name made lowercase.
    fechaIngreso = models.DateTimeField(db_column='FECHAINGRESO', blank=True, null=True)  # Field name made lowercase.
    sueldo = models.FloatField(db_column='SUELDO', blank=True, null=True)  # Field name made lowercase.
    estadoCivil = models.CharField(db_column='ESTADOCIVIL', max_length=1, blank=True)  # Field name made lowercase.
    fechaNacimiento = models.DateTimeField(db_column='FECHANACIMIENTO', blank=True,
                                           null=True)  # Field name made lowercase.
    comentario = models.CharField(db_column='COMENTARIO', max_length=999, blank=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=10, blank=True)  # Field name made lowercase.
    idVendedor = models.IntegerField(db_column='IDVENDEDOR', blank=True, null=True)  # Field name made lowercase.
    idTipoPrecio = models.IntegerField(db_column='IDTIPOPRECIO', blank=True, null=True)  # Field name made lowercase.
    aplicarRetdgr = models.SmallIntegerField(db_column='APLICARRETDGR', blank=True,
                                             null=True)  # Field name made lowercase.
    idGrupo = models.IntegerField(db_column='IDGRUPO', blank=True, null=True)  # Field name made lowercase.
    marca = models.SmallIntegerField(db_column='MARCA', blank=True, null=True)  # Field name made lowercase.
    orden = models.IntegerField(db_column='ORDEN', blank=True, null=True)  # Field name made lowercase.
    telReferencia = models.IntegerField(db_column='TELREFERENCIA', blank=True, null=True)  # Field name made lowercase.
    cpLaboral = models.CharField(db_column='CP_LABORAL', max_length=11, blank=True)  # Field name made lowercase.
    legajo = models.CharField(db_column='LEGAJO', max_length=19, blank=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='CARGO', max_length=19, blank=True)  # Field name made lowercase.
    categoria = models.CharField(db_column='CATEGORIA', max_length=19, blank=True)  # Field name made lowercase.
    idCalle = models.IntegerField(db_column='IDCALLE', blank=True, null=True)  # Field name made lowercase.
    altura = models.CharField(db_column='ALTURA', max_length=29, blank=True)  # Field name made lowercase.
    idBarrio = models.IntegerField(db_column='IDBARRIO', blank=True, null=True)  # Field name made lowercase.
    idEntre1 = models.IntegerField(db_column='IDENTRE1', blank=True, null=True)  # Field name made lowercase.
    idEntre2 = models.IntegerField(db_column='IDENTRE2', blank=True, null=True)  # Field name made lowercase.
    aplicarBonificacion = models.CharField(db_column='APLICARBONIFICACION', max_length=1,
                                           blank=True)  # Field name made lowercase.
    clientePreferencial = models.SmallIntegerField(db_column='CLIENTEPREFERENCIAL', blank=True,
                                                   null=True)  # Field name made lowercase.
    codClientePreferencial = models.CharField(db_column='CODCLIENTEPREFERENCIAL', max_length=20,
                                              blank=True)  # Field name made lowercase.
    puntosAcumulados = models.IntegerField(db_column='PUNTOSACUMULADOS', blank=True,
                                           null=True)  # Field name made lowercase.
    recargos = models.FloatField(db_column='RECARGOS', blank=True, null=True)  # Field name made lowercase.
    situacion = models.SmallIntegerField(db_column='SITUACION', blank=True, null=True)  # Field name made lowercase.
    idClasificacion = models.IntegerField(db_column='IDCLASIFICACION', blank=True,
                                          null=True)  # Field name made lowercase.
    aplicarCostoOperativo = models.SmallIntegerField(db_column='APLICARCOSTOOPERATIVO', blank=True,
                                                     null=True)  # Field name made lowercase.
    puestoId = models.CharField(db_column='PUESTO_ID', max_length=30, blank=True)  # Field name made lowercase.
    usuarioId = models.CharField(db_column='USUARIO_ID', max_length=20, blank=True)  # Field name made lowercase.
    fechaUpdate = models.DateTimeField(db_column='FECHA_UPDATE', blank=True, null=True)  # Field name made lowercase.
    noAplicarPromociones = models.SmallIntegerField(db_column='NOAPLICARPROMOCIONES', blank=True,
                                                    null=True)  # Field name made lowercase.
    diasVencimientoCuentaCorriente = models.SmallIntegerField(db_column='DIASVENCIMIENTOCUENTACORRIENTE', blank=True,
                                                              null=True)  # Field name made lowercase.
    restringirVentaConSaldosPendientes = models.SmallIntegerField(db_column='RESTRINGIRVENTACONSALDOSPENDIENTES',
                                                                  blank=True, null=True)  # Field name made lowercase.
    userDef_0 = models.CharField(db_column='UserDef_0', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    userDef_1 = models.CharField(db_column='UserDef_1', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    userDef_2 = models.CharField(db_column='UserDef_2', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    userDef_3 = models.CharField(db_column='UserDef_3', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    userDef_4 = models.CharField(db_column='UserDef_4', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    userDef_5 = models.CharField(db_column='UserDef_5', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    idcobrador = models.IntegerField(db_column='IDCobrador', blank=True, null=True)  # Field name made lowercase.

    """
    def __init__(self, dni, nombre, fechaNacimiento, domicilio, telefono, usuario):
        super(Cliente, self).__init__()
        self.nroDoc = dni
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento
        self.domicilio = domicilio
        self.telefono = telefono
        self.nroUsuario = usuario
    """

    def __unicode__(self):
        return self.nombre

    def get_usuario(self):
        return self.nroUsuario

    def get_password(self):
        return self.nroUsuario.password

    def get_email(self):
        return self.email

    def get_fechaNacimiento(self):
        return self.fechaNacimiento.strftime('%d-%m-%Y')

    def set_usuario(self, usuario):
        self.nroUsuario = usuario

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_dni(self, dni):
        self.nroDoc = dni

    def set_fechaNacimiento(self, fecha):
        self.fechaNacimiento = fecha

    def set_email(self, email):
        self.email = email

    def set_domicilio(self, domicilio):
        self.domicilio = domicilio

    def set_telefono(self, telefono):
        self.telefono = telefono

    class Meta:
        db_table = 'FACT_0004'

class Persona(models.Model):
    nroUsuario = models.OneToOneField(User)
    nombre = models.CharField(max_length=40, null=False)
    dni = models.CharField(max_length=8, null=False, default=0)
    email = models.EmailField(max_length=255, blank=True, unique=True, null=False, default='')
    fechaNacimiento = models.DateTimeField(blank=True, null=True)
    domicilio = models.CharField(max_length=254, blank=True, default='')
    telefono = models.CharField(max_length=254, blank=True, default='')

    class Meta:
        abstract = 'True'

    def get_usuario(self):
        return self.nroUsuario

    def set_dni(self, dni):
        self.dni = dni

    def set_usuario(self, usuario):
        self.nroUsuario = usuario

    def get_password(self):
        return self.nroUsuario.password

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_fechaNacimiento(self, fechaNacimiento):
        self.fechaNacimiento = fechaNacimiento

    def set_email(self, email):
        self.email = email

    def set_domicilio(self, domicilio):
        self.domicilio = domicilio

    def set_telefono(self, telefono):
        self.telefono = telefono

    def __unicode__(self):
        return self.nombre

class Empleado(Persona):
    admin = models.BooleanField(default=False)

    def set_admin(self, bool):
        self.admin = bool

    def is_admin(self):
        return self.admin

    class Meta:
        db_table = 'Empleados'
        verbose_name_plural = 'Empleados'
        permissions = [('cambiar_cont', 'Puede cambiar su contrasena'), ('view_facturas', 'Puede ver las facutras de los clientes'),
                       ('view_lista_cliente', 'Puede ver la lista de clientes'),
                       ('view_detalle_cliente', 'Puede ver detalle cliente'), ('update_cliente', 'Puede modificar cliente'),
                       ('agregar_cliente', 'Puede agregar cliente'), ('del_cliente', 'Puede eliminar cliente'),
                       ('view_perfil_empleado', 'Puede ver su perfil de empleado')
                       ]

class Cliente(Persona):

    class Meta:
        db_table = 'Clientes'
        verbose_name_plural = 'Clientes'
        permissions = [('cambiar_cont', 'Puede cambiar su contrasena'), ('view_perfil_cliente', 'Puede ver su perfil de cliente'),
                       ('view_facturas_cliente', 'Puede ver sus facturas')]

class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'Tags'
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class EntryQuerySet(models.QuerySet):
        def published(self):
            return self.filter(publish=True)


class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    objects = EntryQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug": self.slug})

    class Meta:
        db_table = 'Entradas'
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"


# @receiver(post_delete, sender=Administrador)
# def eliminar_usuario_admin(sender, **kwargs):
#     eliminar_usuario(**kwargs)

@receiver(post_delete, sender=Empleado)
def eliminar_usuario_empleado(sender, **kwargs):
    eliminar_usuario(**kwargs)

@receiver(post_delete, sender=Cliente)
def eliminar_usuario_cliente(sender, **kwargs):
    eliminar_usuario(**kwargs)

def eliminar_usuario(**kwargs):
    model = kwargs.get('instance')
    try:
        u = model.get_usuario()
    except User.DoesNotExist:
        return
    u.delete()
    return

