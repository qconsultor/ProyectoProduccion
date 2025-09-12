# En produccion/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- URL Principal y Dashboard ---
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('dashboard/', views.dashboard_produccion, name='dashboard'),
    
    # --- Órdenes de Producción ---
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('orden/nueva/', views.crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('orden/<int:orden_id>/editar/', views.editar_orden, name='editar_orden'),
    path('orden/<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),

    # --- Requisiciones ---
    path('requisiciones/', views.lista_requisiciones, name='lista_requisiciones'),
    path('requisicion/nueva/', views.crear_requisicion, name='crear_requisicion'),
    path('requisicion/<int:req_id>/', views.detalle_requisicion, name='detalle_requisicion'),
    path('requisicion/<int:req_id>/editar/', views.editar_requisicion, name='editar_requisicion'),
    path('requisicion/<int:req_id>/eliminar/', views.eliminar_requisicion, name='eliminar_requisicion'),

    # --- Controles de Proceso ---
    path('controles/', views.lista_controles, name='lista_controles'),
    path('control/nuevo/', views.crear_control, name='crear_control'),
    path('control/<int:control_id>/', views.detalle_control, name='detalle_control'),
    path('control/<int:control_id>/editar/', views.editar_control, name='editar_control'),
    path('control/<int:control_id>/eliminar/', views.eliminar_control, name='eliminar_control'),

    # --- Cortes de Bobina ---
    path('cortes/', views.lista_cortes, name='lista_cortes'),
    path('corte/nuevo/', views.crear_corte, name='crear_corte'),
    path('corte/<int:corte_id>/', views.detalle_corte, name='detalle_corte'),
    path('corte/<int:corte_id>/editar/', views.editar_corte, name='editar_corte'),
    path('corte/<int:corte_id>/eliminar/', views.eliminar_corte, name='eliminar_corte'),

    # --- Reportes Diarios ---
    path('reportes-diarios/', views.lista_reportes_diarios, name='lista_reportes_diarios'),
    path('reporte-diario/nuevo/', views.crear_reporte_diario, name='crear_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/', views.detalle_reporte_diario, name='detalle_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/editar/', views.editar_reporte_diario, name='editar_reporte_diario'),
    path('reporte-diario/<int:reporte_id>/eliminar/', views.eliminar_reporte_diario, name='eliminar_reporte_diario'),

    # --- Notas de Ingreso ---
    path('notas-ingreso/', views.lista_notas_ingreso, name='lista_notas_ingreso'),
    path('nota-ingreso/nueva/', views.crear_nota_ingreso, name='crear_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/', views.detalle_nota_ingreso, name='detalle_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/editar/', views.editar_nota_ingreso, name='editar_nota_ingreso'),
    path('nota-ingreso/<int:nota_id>/eliminar/', views.eliminar_nota_ingreso, name='eliminar_nota_ingreso'),

    # --- Productos ---
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/ingreso/', views.ingreso_producto, name='ingreso_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),

    # --- Reportes ---
    path('reportes/kardex/', views.reporte_kardex, name='reporte_kardex'),
    path('reportes/kardex/imprimir/', views.reporte_kardex_imprimir, name='reporte_kardex_imprimir'),
    path('reportes/movimientos/', views.reporte_movimientos, name='reporte_movimientos'),

    # --- URLs de APIs (para JavaScript) ---
    path('api/buscar-bobinas/', views.buscar_bobinas_api, name='buscar_bobinas_api'),
    path('api/buscar-papel/', views.buscar_papel_api, name='buscar_papel_api'),
    path('api/verificar-producto/', views.verificar_producto_api, name='verificar_producto_api'),
    path('api/buscar-productos/', views.buscar_productos_api, name='buscar_productos_api'),
    path('api/get-producto-detalle/', views.get_producto_detalle_api, name='get_producto_detalle_api'),
    path('api/get-siguiente-numero/', views.get_siguiente_numero_api, name='get_siguiente_numero_api'),

    # --- AÑADE ESTA NUEVA SECCIÓN ---
    # --- Consulta de Movimientos de Inventario ---
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimientos/detalle/<str:tipo_documento>/<int:numero>/', views.detalle_movimiento, name='detalle_movimiento'),
]



# # En produccion/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.lista_ordenes, name='lista_ordenes'),
#     # --- AÑADE ESTA LÍNEA ---
#     path('dashboard/', views.dashboard_produccion, name='dashboard'),
#     # --- Órdenes de Producción ---
#     path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
#     path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
#     path('orden/nueva/', views.crear_orden, name='crear_orden'),
#     path('orden/<int:orden_id>/editar/', views.editar_orden, name='editar_orden'),
#     path('orden/<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),

#     # --- Requisiciones ---
#     path('requisiciones/', views.lista_requisiciones, name='lista_requisiciones'),
#     path('requisicion/<int:req_id>/', views.detalle_requisicion, name='detalle_requisicion'),
#     path('requisicion/nueva/', views.crear_requisicion, name='crear_requisicion'),
#     path('requisicion/<int:req_id>/editar/', views.editar_requisicion, name='editar_requisicion'),
#     path('requisicion/<int:req_id>/eliminar/', views.eliminar_requisicion, name='eliminar_requisicion'),

#     # --- Controles de Proceso ---
#     path('controles/', views.lista_controles, name='lista_controles'),
#     path('control/<int:control_id>/', views.detalle_control, name='detalle_control'),
#     path('control/nuevo/', views.crear_control, name='crear_control'),
#     path('control/<int:control_id>/editar/', views.editar_control, name='editar_control'),
#     path('control/<int:control_id>/eliminar/', views.eliminar_control, name='eliminar_control'),

#     # --- Cortes de Bobina ---
#     path('cortes/', views.lista_cortes, name='lista_cortes'),
#     path('corte/nuevo/', views.crear_corte, name='crear_corte'),
#     path('corte/<int:corte_id>/', views.detalle_corte, name='detalle_corte'),
#     path('corte/<int:corte_id>/editar/', views.editar_corte, name='editar_corte'),
#     path('corte/<int:corte_id>/eliminar/', views.eliminar_corte, name='eliminar_corte'),
#     path('api/buscar-bobinas/', views.buscar_bobinas_api, name='buscar_bobinas_api'),
#     # ... otras urls DAVID
#     #path('corte/editar/<int:reporte_id>/', views.editar_reporte, name='editar_reporte'),

#     # --- Reportes Diarios ---
#     path('reportes-diarios/', views.lista_reportes_diarios, name='lista_reportes_diarios'),
#     path('reporte-diario/<int:reporte_id>/', views.detalle_reporte_diario, name='detalle_reporte_diario'),
#     path('reporte-diario/nuevo/', views.crear_reporte_diario, name='crear_reporte_diario'),
#     path('reporte-diario/<int:reporte_id>/editar/', views.editar_reporte_diario, name='editar_reporte_diario'),
#     path('reporte-diario/<int:reporte_id>/eliminar/', views.eliminar_reporte_diario, name='eliminar_reporte_diario'),

#     # --- Notas de Ingreso ---
#     path('notas-ingreso/', views.lista_notas_ingreso, name='lista_notas_ingreso'),
#     path('nota-ingreso/<int:nota_id>/', views.detalle_nota_ingreso, name='detalle_nota_ingreso'),
#     path('nota-ingreso/nueva/', views.crear_nota_ingreso, name='crear_nota_ingreso'),
#     path('nota-ingreso/<int:nota_id>/editar/', views.editar_nota_ingreso, name='editar_nota_ingreso'),
#     path('nota-ingreso/<int:nota_id>/eliminar/', views.eliminar_nota_ingreso, name='eliminar_nota_ingreso'),

#     # --- Reportes ---
#     path('reportes/kardex/', views.reporte_kardex, name='reporte_kardex'),
#     path('reportes/kardex/imprimir/', views.reporte_kardex_imprimir, name='reporte_kardex_imprimir'),

#     # --- AGREGA ESTA LÍNEA ---
#     path('api/buscar-papel/', views.buscar_papel_api, name='buscar_papel_api'),
#     # ...

#     #30082025
#     # URLs para el CRUD de Productos
#     path('productos/', views.lista_productos, name='lista_productos'),
#     path('productos/nuevo/', views.crear_producto, name='crear_producto'),
#     path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),

#     # URL para la API de verificación (AJAX)
#     path('api/verificar-producto/', views.verificar_producto_api, name='verificar_producto_api'),

#     # --- AÑADE ESTA NUEVA LÍNEA ---
#     path('api/buscar-productos/', views.buscar_productos_api, name='buscar_productos_api'),

#     # --- AÑADE ESTAS DOS NUEVAS LÍNEAS ---
#     path('productos/ingreso/', views.ingreso_producto, name='ingreso_producto'),
#     path('api/get-producto-detalle/', views.get_producto_detalle_api, name='get_producto_detalle_api'),

#     # --- AÑADE ESTA LÍNEA NUEVA ---
#     path('api/get-siguiente-numero/', views.get_siguiente_numero_api, name='get_siguiente_numero_api'),    
#     # --- URLs de APIs ---
#     path('api/buscar-papel/', views.buscar_papel_api, name='buscar_papel_api'),
# ]