# produccion/models_liquidacion.py
from django.db import models

class Liquidacion(models.Model):
    cliente_id = models.CharField(max_length=50)  # referencia lógica a RQ.dbo.clientes(CODIGO)
    consignacion_id = models.IntegerField(null=True, blank=True)  # ID de la consignación origen
    fecha = models.DateField(auto_now_add=False)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'produccion_liquidacion'
        ordering = ['-id']

    def __str__(self):
        return f"Liquidación #{self.id} - {self.referencia or ''}"

class LiquidacionDetalle(models.Model):
    liquidacion = models.ForeignKey(Liquidacion, on_delete=models.CASCADE, related_name='detalles')
    consignacion_detalle_id = models.IntegerField(null=True, blank=True)  # ID del detalle de consignación
    producto_id = models.IntegerField()  # orden (PK) del producto en RQ
    cantidad_consignada = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cantidad original
    cantidad_devuelta = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Devoluciones
    cantidad_vendida = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Ventas
    cantidad_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Saldo
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_linea = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'produccion_liquidaciondetalle'

    def __str__(self):
        return f"Producto {self.producto_id} - Vendido: {self.cantidad_vendida}"
