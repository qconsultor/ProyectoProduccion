from django.db import models
from django.utils import timezone

# ========================================================================
# MODELOS DE PRODUCCIÓN (EXISTENTES)
# ========================================================================

class OrdenProduccion(models.Model):
    ESTADOS_PRODUCCION = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('DETENIDO', 'Detenido'),
    ]
    status = models.CharField(max_length=20, choices=ESTADOS_PRODUCCION, default='PENDIENTE', verbose_name="Estado")
    numero_orden = models.CharField(max_length=50, unique=True, blank=True, null=True)
    fecha = models.DateField()
    producto_a_elaborar = models.CharField(max_length=255)
    cantidad_a_producir = models.IntegerField()
    cantidad_hojas_por_ejemplar = models.IntegerField(blank=True, null=True)
    tiraje_total = models.IntegerField(blank=True, null=True)
    numero_de_resmas = models.CharField(max_length=100, blank=True, null=True)
    medida_de_corte = models.CharField(max_length=100, blank=True, null=True)
    tamano = models.CharField(max_length=100, blank=True, null=True)
    papel = models.CharField(max_length=100, blank=True, null=True)
    base = models.CharField(max_length=100, blank=True, null=True)
    total_planchas = models.IntegerField(blank=True, null=True)
    numero_de_pliegos = models.IntegerField(blank=True, null=True)
    medida_de_plancha = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.numero_orden)


class OrdenProduccionDetalle(models.Model):
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='detalles')
    montaje = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    impresion_full = models.BooleanField(default=False)
    impresion_t = models.BooleanField(default=False)
    impresion_r = models.BooleanField(default=False)
    operario = models.CharField(max_length=100, blank=True, null=True)
    maquina = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    total_impresion_programado = models.IntegerField(blank=True, null=True)
    total_impresion_real = models.IntegerField(blank=True, null=True)


class RequisicionEncabezado(models.Model):
    numero_requisicion = models.IntegerField(unique=True)
    producto_a_elaborar = models.CharField(max_length=255)
    fecha = models.DateField()
    solicitado_por = models.CharField(max_length=100, blank=True, null=True)
    autorizado_por = models.CharField(max_length=100, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisiciones')

    def __str__(self):
        return f"Requisición N° {self.numero_requisicion}"


class RequisicionDetalle(models.Model):
    requisicion = models.ForeignKey(RequisicionEncabezado, on_delete=models.CASCADE, related_name='detalles')
    producto_solicitado = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=255, blank=True, null=True)


class ControlProceso(models.Model):
    nombre_del_libro = models.CharField(max_length=255)
    temporada_anio = models.IntegerField()
    tiraje = models.IntegerField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    elaborado_por = models.CharField(max_length=100, blank=True, null=True)
    revisado_por = models.CharField(max_length=100, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='controles')

    def __str__(self):
        return f"Control de Proceso para: {self.nombre_del_libro} ({self.temporada_anio})"


class ControlProcesoDetalle(models.Model):
    control_proceso = models.ForeignKey(ControlProceso, on_delete=models.CASCADE, related_name='detalles')
    fecha = models.DateField()
    turno = models.IntegerField()
    compaginado = models.IntegerField(blank=True, null=True)
    doblado_libro = models.IntegerField(blank=True, null=True)
    doblado_portada = models.IntegerField(blank=True, null=True)
    engrapado = models.IntegerField(blank=True, null=True)
    pegado = models.IntegerField(blank=True, null=True)
    refilado = models.IntegerField(blank=True, null=True)
    empacado = models.IntegerField(blank=True, null=True)
    unidades = models.IntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)


class CorteDeBobina(models.Model):
    numero_reporte = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    nombre_operario = models.CharField(max_length=255)
    ancho_bobina = models.CharField(max_length=50, blank=True, null=True)
    medida_de_corte = models.CharField(max_length=50, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='cortes')

    def __str__(self):
        return f"Corte de Bobina N° {self.numero_reporte} - {self.nombre_operario}"


class CorteDeBobinaDetalle(models.Model):
    corte_de_bobina = models.ForeignKey(CorteDeBobina, on_delete=models.CASCADE, related_name='detalles')
    codigo_bobina_usada = models.CharField(max_length=50, verbose_name="Bobina Usada")
    codigo_pliego_producido_1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pliego Producido 1")
    cantidad_pliegos_1 = models.IntegerField(default=0, verbose_name="Cantidad Pliegos 1")
    resmas_producidas_1 = models.IntegerField(default=0, blank=True, null=True, verbose_name="Resmas Producidas 1")
    codigo_pliego_producido_2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pliego Producido 2")
    cantidad_pliegos_2 = models.IntegerField(default=0, verbose_name="Cantidad Pliegos 2")
    resmas_producidas_2 = models.IntegerField(default=0, blank=True, null=True, verbose_name="Resmas Producidas 2")
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detalle para corte {self.corte_de_bobina.numero_reporte}"


class ReporteDiarioProductoTerminado(models.Model):
    nombre_encargado = models.CharField(max_length=255)
    fecha = models.DateField()
    turno = models.CharField(max_length=50)
    elaborado_por = models.CharField(max_length=255, blank=True, null=True)
    revisado_por = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Reporte Diario del {self.fecha} (Turno {self.turno}) por {self.nombre_encargado}"


class ReporteDiarioDetalle(models.Model):
    reporte_diario = models.ForeignKey(ReporteDiarioProductoTerminado, on_delete=models.CASCADE, related_name='detalles')
    nombre_producto = models.CharField(max_length=255)
    compaginado = models.IntegerField(blank=True, null=True)
    doblado_libro = models.IntegerField(blank=True, null=True)
    doblado_portada = models.IntegerField(blank=True, null=True)
    engrapado = models.IntegerField(blank=True, null=True)
    empacado = models.IntegerField(blank=True, null=True)


class NotaIngresoProductoTerminado(models.Model):
    numero_nota = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    elaborado_por = models.CharField(max_length=255, blank=True, null=True)
    recibido_por = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Nota de Ingreso N° {self.numero_nota}"


class NotaIngresoDetalle(models.Model):
    nota_ingreso = models.ForeignKey(NotaIngresoProductoTerminado, on_delete=models.CASCADE, related_name='detalles')
    codigo = models.CharField(max_length=100)
    descripcion_producto = models.CharField(max_length=255)
    paquetes = models.CharField(max_length=100, blank=True, null=True)
    unidades = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)


# ========================================================================
# MODELOS DE CONEXIÓN A BD 'RQ'
# ========================================================================

class ProductoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(idsucursal=10)


class Producto(models.Model):
    orden = models.AutoField(primary_key=True, db_column='orden')
    codigo = models.CharField(max_length=50, db_column='codigo', unique=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    nombre3 = models.CharField(max_length=50, blank=True, null=True, db_column='nombre3')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='cantidad')
    idsucursal = models.IntegerField(editable=False, db_column='idsucursal')
    venta = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='venta')

    class Meta:
        managed = False
        db_table = 'productos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Kardex(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True, db_column='regi_orden')
    codigo = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    documento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Documento de Referencia")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    idsucursal = models.IntegerField()
    numero = models.IntegerField(blank=True, null=True, verbose_name="Número de Referencia", db_column='NUMERO')

    class Meta:
        managed = False
        db_table = 'kardex'

    def __str__(self):
        return f"Movimiento de {self.producto.nombre} el {self.fecha.strftime('%Y-%m-%d')}"


# ========================================================================
# MODELOS DE CONSIGNACIONES
# ========================================================================

class Cliente(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=255)
    nombrecomercial = models.CharField(max_length=255, blank=True, null=True)
    saldo = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    empresa = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clientes'
        app_label = 'produccion'

    def __str__(self):
        return self.nombre or f"[Sin nombre] {self.codigo}"


class Consignacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    referencia = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # ✅ Cambiar de IntegerField a ForeignKey
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.PROTECT,
        db_column='cliente_id',
        to_field='codigo',
        db_constraint=False  # 👈 muy útil si Cliente está en otra base
    )
    
    # cliente = models.ForeignKey(
    #     'Cliente',
    #     on_delete=models.PROTECT,
    #     db_column='cliente_id',
    #     db_constraint=False
    # )


    class Meta:
        managed = False
        db_table = 'produccion_consignacion'

    def __str__(self):
        return f"Consignación {self.referencia} - {self.cliente.nombre}"


class ConsignacionDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total_linea = models.DecimalField(max_digits=12, decimal_places=2)

    consignacion = models.ForeignKey(
        'Consignacion',
        related_name='detalles',
        on_delete=models.CASCADE,
        db_column='consignacion_id'
    )

    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT,
        db_constraint=False,
        db_column='producto_id'
    )

    class Meta:
        #managed = True   # 👈 TEMPORALMENTE
        managed = False    # 👈 lo regresamos
        db_table = 'produccion_consignaciondetalle'   # ✅ nombre correcto



