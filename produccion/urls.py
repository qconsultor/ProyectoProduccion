from django.urls import path
from . import views # Importa las vistas que crearemos en el siguiente paso

urlpatterns = [
    # Esta URL corresponde a la raíz de la app, ej: /produccion/
    path('', views.lista_ordenes, name='lista_ordenes'),# AGREGA ESTA NUEVA LÍNEA PARA LOS DETALLES
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    # AGREGA ESTA NUEVA LÍNEA PARA EL FORMULARIO
    path('orden/nueva/', views.crear_orden, name='crear_orden'),
    # AGREGA ESTA NUEVA LÍNEA PARA EDITAR
    path('orden/<int:orden_id>/editar/', views.editar_orden, name='editar_orden'),
    # AGREGA ESTA NUEVA LÍNEA PARA ELIMINAR
    path('orden/<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),

    #
    # --- URLs para Requisiciones (BLOQUE CORREGIDO) ---
    # La lista sí puede ser plural
    path('requisiciones/', views.lista_requisiciones, name='lista_requisiciones'),

    # Las acciones sobre un objeto, en singular para que coincidan con las vistas
    path('requisicion/<int:req_id>/', views.detalle_requisicion, name='detalle_requisicion'),
    path('requisicion/nueva/', views.crear_requisicion, name='crear_requisicion'),
    path('requisicion/<int:req_id>/editar/', views.editar_requisicion, name='editar_requisicion'),
    path('requisicion/<int:req_id>/eliminar/', views.eliminar_requisicion, name='eliminar_requisicion'),

    # --- AGREGA ESTE NUEVO BLOQUE DE URLS ---
    path('controles/', views.lista_controles, name='lista_controles'),
    path('control/<int:control_id>/', views.detalle_control, name='detalle_control'),
    path('control/nuevo/', views.crear_control, name='crear_control'),
    path('control/<int:control_id>/editar/', views.editar_control, name='editar_control'),
    path('control/<int:control_id>/eliminar/', views.eliminar_control, name='eliminar_control'),

    # --- AGREGA ESTE NUEVO BLOQUE DE URLS ---
    path('reportes-diarios/', views.lista_reportes_diarios, name='lista_reportes_diarios'),
    path('reporte-diario/<int:reporte_id>/', views.detalle_reporte_diario, name='detalle_reporte_diario'),
    path('reporte-diario/nuevo/', views.crear_reporte_diario, name='crear_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/editar/', views.editar_reporte_diario, name='editar_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/eliminar/', views.eliminar_reporte_diario, name='eliminar_reporte_diario'),

    # --- AGREGA ESTE NUEVO BLOQUE DE URLS ---
    path('notas-ingreso/', views.lista_notas_ingreso, name='lista_notas_ingreso'),
    path('nota-ingreso/<int:nota_id>/', views.detalle_nota_ingreso, name='detalle_nota_ingreso'),
    path('nota-ingreso/nueva/', views.crear_nota_ingreso, name='crear_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/editar/', views.editar_nota_ingreso, name='editar_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/eliminar/', views.eliminar_nota_ingreso, name='eliminar_nota_ingreso'),

    #---REPORTES 
    path('reportes/kardex/', views.reporte_kardex, name='reporte_kardex'),

    # AGREGA ESTA NUEVA LÍNEA
    path('reportes/kardex/imprimir/', views.reporte_kardex_imprimir, name='reporte_kardex_imprimir'),
]