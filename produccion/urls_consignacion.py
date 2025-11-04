# produccion/urls_consignacion.py
from django.urls import path
from . import views_consignacion

app_name = 'consignacion'

urlpatterns = [
    # CLIENTES
    path('clientes/', views_consignacion.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views_consignacion.crear_cliente, name='crear_cliente'),
    path('clientes/<str:pk>/editar/', views_consignacion.editar_cliente, name='editar_cliente'),
    path('clientes/<str:pk>/eliminar/', views_consignacion.eliminar_cliente, name='eliminar_cliente'),

    # CONSIGNACIONES
    path('', views_consignacion.lista_consignaciones, name='lista_consignaciones'),
    path('nueva/', views_consignacion.crear_consignacion, name='crear_consignacion'),
    path('<int:pk>/', views_consignacion.detalle_consignacion, name='detalle_consignacion'),
    path('<int:pk>/editar/', views_consignacion.editar_consignacion, name='editar_consignacion'),
    path('<int:pk>/eliminar/', views_consignacion.eliminar_consignacion, name='eliminar_consignacion'),
    path('<int:consignacion_id>/devolucion/', views_consignacion.registrar_devolucion, name='registrar_devolucion'),
    path('<int:pk>/editar/', views_consignacion.editar_consignacion, name='editar_consignacion'),

    # API
    path('api/buscar-clientes/', views_consignacion.buscar_clientes_api, name='buscar_clientes_api'),
    path('api/buscar-productos-consignacion/', views_consignacion.buscar_productos_consignacion_api, name='buscar_productos_consignacion_api'),
    path('api/get-producto-detalle-consignacion/', views_consignacion.get_producto_detalle_consignacion_api, name='get_producto_detalle_consignacion_api'),
]
