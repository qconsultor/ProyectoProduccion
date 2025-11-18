# produccion/urls_liquidacion.py
from django.urls import path
from . import views_liquidacion as views_liquidacion

app_name = 'liquidacion'

urlpatterns = [
    # Vistas de consulta
    path('', views_liquidacion.listar_liquidaciones, name='listar'),
    path('<int:pk>/', views_liquidacion.ver_liquidacion, name='ver'),
    
    # Vistas de creación/edición
    path('nueva/', views_liquidacion.crear_liquidacion, name='nueva'),
    path('editar/<int:pk>/', views_liquidacion.editar_liquidacion, name='editar'),
    
    # APIs
    path('api/buscar-productos/', views_liquidacion.buscar_productos_liquidacion_api, name='buscar_productos_api'),
    path('api/get-producto-detalle/', views_liquidacion.get_producto_detalle_liquidacion_api, name='get_producto_detalle_api'),
    
    # APIs nuevas para consignaciones
    path('api/consignaciones-por-cliente/', views_liquidacion.api_consignaciones_por_cliente, name='api_consignaciones_por_cliente'),
    path('api/detalle-consignacion-pendiente/', views_liquidacion.api_detalle_consignacion_pendiente, name='api_detalle_consignacion_pendiente'),
    
    # API para correlativo automático
    path('api/siguiente-referencia/', views_liquidacion.api_siguiente_referencia, name='api_siguiente_referencia'),
    
    # Exportaciones
    path('<int:pk>/exportar/pdf/', views_liquidacion.exportar_pdf, name='exportar_pdf'),
    path('<int:pk>/exportar/excel/', views_liquidacion.exportar_excel, name='exportar_excel'),
    path('<int:pk>/exportar/word/', views_liquidacion.exportar_word, name='exportar_word'),
]
