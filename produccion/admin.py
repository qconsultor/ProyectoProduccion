from django.contrib import admin
from .models import (
    RequisicionEncabezado, 
    RequisicionDetalle,
    OrdenProduccion,
    OrdenProduccionDetalle,
    ControlProceso,
    ControlProcesoDetalle,
    CorteDeBobina,
    CorteDeBobinaDetalle,
    ReporteDiarioProductoTerminado,
    ReporteDiarioDetalle,
    NotaIngresoProductoTerminado,
    NotaIngresoDetalle,
)

class RequisicionDetalleInline(admin.TabularInline):
    model = RequisicionDetalle
    extra = 1 

@admin.register(RequisicionEncabezado)
class RequisicionEncabezadoAdmin(admin.ModelAdmin):
    list_display = ('numero_requisicion', 'producto_a_elaborar', 'fecha', 'solicitado_por')
    inlines = [RequisicionDetalleInline]

class OrdenProduccionDetalleInline(admin.TabularInline):
    model = OrdenProduccionDetalle
    extra = 1

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'producto_a_elaborar', 'cantidad_a_producir', 'fecha')
    inlines = [OrdenProduccionDetalleInline]

class ControlProcesoDetalleInline(admin.TabularInline):
    model = ControlProcesoDetalle
    extra = 1

@admin.register(ControlProceso)
class ControlProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre_del_libro', 'temporada_anio', 'cantidad')
    inlines = [ControlProcesoDetalleInline]

class CorteDeBobinaDetalleInline(admin.TabularInline):
    model = CorteDeBobinaDetalle
    extra = 1

@admin.register(CorteDeBobina)
class CorteDeBobinaAdmin(admin.ModelAdmin):
    list_display = ('numero_reporte', 'fecha', 'nombre_operario')
    inlines = [CorteDeBobinaDetalleInline]

class ReporteDiarioDetalleInline(admin.TabularInline):
    model = ReporteDiarioDetalle
    extra = 1

@admin.register(ReporteDiarioProductoTerminado)
class ReporteDiarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'turno', 'nombre_encargado')
    inlines = [ReporteDiarioDetalleInline]

class NotaIngresoDetalleInline(admin.TabularInline):
    model = NotaIngresoDetalle
    extra = 1

@admin.register(NotaIngresoProductoTerminado)
class NotaIngresoAdmin(admin.ModelAdmin):
    list_display = ('numero_nota', 'fecha', 'elaborado_por', 'recibido_por')
    inlines = [NotaIngresoDetalleInline]