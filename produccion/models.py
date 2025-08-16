from django.db import models

# --- MODELOS EXISTENTES ---

class RequisicionEncabezado(models.Model):
    numero_requisicion = models.IntegerField(unique=True)
    producto_a_elaborar = models.CharField(max_length=255)
    fecha = models.DateField()
    solicitado_por = models.CharField(max_length=100, blank=True, null=True)
    autorizado_por = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Requisición N° {self.numero_requisicion}"

class RequisicionDetalle(models.Model):
    requisicion = models.ForeignKey(RequisicionEncabezado, on_delete=models.CASCADE, related_name='detalles')
    producto_solicitado = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=255, blank=True, null=True)

class OrdenProduccion(models.Model):
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
        return f"Orden N° {self.numero_orden} - {self.producto_a_elaborar}"

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

class ControlProceso(models.Model):
    nombre_del_libro = models.CharField(max_length=255)
    temporada_anio = models.IntegerField()
    tiraje = models.IntegerField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    elaborado_por = models.CharField(max_length=100, blank=True, null=True)
    revisado_por = models.CharField(max_length=100, blank=True, null=True)

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

# --- NUEVOS MODELOS ---

class CorteDeBobina(models.Model):
    numero_reporte = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    nombre_operario = models.CharField(max_length=255)
    ancho_bobina = models.CharField(max_length=50, blank=True, null=True)
    medida_de_corte = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Corte de Bobina N° {self.numero_reporte} - {self.nombre_operario}"

class CorteDeBobinaDetalle(models.Model):
    corte_de_bobina = models.ForeignKey(CorteDeBobina, on_delete=models.CASCADE, related_name='detalles')
    codigo_bobina = models.CharField(max_length=100)
    pliegos = models.IntegerField()
    resmas = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

class ReporteDiarioProductoTerminado(models.Model):
    nombre_encargado = models.CharField(max_length=255)
    fecha = models.DateField()
    turno = models.CharField(max_length=50) # Mañana / Tarde
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

# Al final de produccion/models.py

# En produccion/models.py

class Producto(models.Model):
    # Le decimos a Django que la llave primaria se llama 'orden'.
    # Usamos BigAutoField porque numeric(14,0) es un número grande que se auto-incrementa.
    # Esto reemplaza el campo 'id' que Django crea por defecto.
    orden = models.BigAutoField(primary_key=True)

    # El resto de los campos que ya definiste
    codigo = models.CharField(max_length=30, unique=True, verbose_name="Codigo")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    idsucursal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'productos' # El nombre real de tu tabla en RQ

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    #regi_orden
class Kardex(models.Model):
    # Este único campo ahora representa AMBAS cosas:
    # 1. La relación con el Producto (ForeignKey).
    # 2. La llave primaria de esta tabla (primary_key=True).
    # 3. Le decimos que la columna en la BD se llama 'regi_orden' (db_column='regi_orden').
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, primary_key=True, db_column='regi_orden')

    # El resto de los campos permanecen igual
    codigo = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    documento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Documento de Referencia")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    idsucursal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kardex'

    def __str__(self):
        return f"Movimiento de {self.producto.nombre} el {self.fecha.strftime('%Y-%m-%d')}" 