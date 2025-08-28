# En produccion/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    # --- AÑADE ESTA LÍNEA ---
    path('dashboard/', views.dashboard_produccion, name='dashboard'),
    # --- Órdenes de Producción ---
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('orden/nueva/', views.crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/editar/', views.editar_orden, name='editar_orden'),
    path('orden/<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),

    # --- Requisiciones ---
    path('requisiciones/', views.lista_requisiciones, name='lista_requisiciones'),
    path('requisicion/<int:req_id>/', views.detalle_requisicion, name='detalle_requisicion'),
    path('requisicion/nueva/', views.crear_requisicion, name='crear_requisicion'),
    path('requisicion/<int:req_id>/editar/', views.editar_requisicion, name='editar_requisicion'),
    path('requisicion/<int:req_id>/eliminar/', views.eliminar_requisicion, name='eliminar_requisicion'),

    # --- Controles de Proceso ---
    path('controles/', views.lista_controles, name='lista_controles'),
    path('control/<int:control_id>/', views.detalle_control, name='detalle_control'),
    path('control/nuevo/', views.crear_control, name='crear_control'),
    path('control/<int:control_id>/editar/', views.editar_control, name='editar_control'),
    path('control/<int:control_id>/eliminar/', views.eliminar_control, name='eliminar_control'),

    # --- Cortes de Bobina ---
    path('cortes/', views.lista_cortes, name='lista_cortes'),
    path('corte/nuevo/', views.crear_corte, name='crear_corte'),
    path('corte/<int:corte_id>/', views.detalle_corte, name='detalle_corte'),
    path('corte/<int:corte_id>/editar/', views.editar_corte, name='editar_corte'),
    path('corte/<int:corte_id>/eliminar/', views.eliminar_corte, name='eliminar_corte'),
    path('api/buscar-bobinas/', views.buscar_bobinas_api, name='buscar_bobinas_api'),
    # ... otras urls DAVID
    #path('corte/editar/<int:reporte_id>/', views.editar_reporte, name='editar_reporte'),

    # --- Reportes Diarios ---
    path('reportes-diarios/', views.lista_reportes_diarios, name='lista_reportes_diarios'),
    path('reporte-diario/<int:reporte_id>/', views.detalle_reporte_diario, name='detalle_reporte_diario'),
    path('reporte-diario/nuevo/', views.crear_reporte_diario, name='crear_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/editar/', views.editar_reporte_diario, name='editar_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/eliminar/', views.eliminar_reporte_diario, name='eliminar_reporte_diario'),

    # --- Notas de Ingreso ---
    path('notas-ingreso/', views.lista_notas_ingreso, name='lista_notas_ingreso'),
    path('nota-ingreso/<int:nota_id>/', views.detalle_nota_ingreso, name='detalle_nota_ingreso'),
    path('nota-ingreso/nueva/', views.crear_nota_ingreso, name='crear_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/editar/', views.editar_nota_ingreso, name='editar_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/eliminar/', views.eliminar_nota_ingreso, name='eliminar_nota_ingreso'),

    # --- Reportes ---
    path('reportes/kardex/', views.reporte_kardex, name='reporte_kardex'),
    path('reportes/kardex/imprimir/', views.reporte_kardex_imprimir, name='reporte_kardex_imprimir'),

    # --- AGREGA ESTA LÍNEA ---
    path('api/buscar-papel/', views.buscar_papel_api, name='buscar_papel_api'),
    # ...
]