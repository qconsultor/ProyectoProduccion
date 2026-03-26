# produccion/integracion_rq.py
"""
Módulo de integración con el sistema de facturación RQ
IMPORTANTE: Solo insertar datos, NO modificar tablas existentes
"""

from django.db import connections
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def insertar_prefactura_rq(liquidacion):
    """
    Inserta una liquidación en las tablas prefactura y prefactura_detalle de RQ
    
    Args:
        liquidacion: Objeto Liquidacion de la base Personal
    
    Returns:
        tuple: (success: bool, message: str, prefactura_id: int or None)
    """
    try:
        # Obtener datos del cliente desde RQ
        cliente = obtener_cliente_rq(liquidacion.cliente_id)
        
        if not cliente:
            # Si no se encuentra, usar datos básicos
            logger.warning(f"Cliente {liquidacion.cliente_id} no encontrado en RQ, usando datos básicos")
            cliente = {
                'codigo': str(liquidacion.cliente_id),
                'nombre': f'Cliente {liquidacion.cliente_id}',
                'direccion': None,
                'nregistro': None,
                'dui': None,
                'nit': None,
                'giro': None,
                'telefono': None,
                'tipocliente': None,
                'codActividad': None,
                'tipoDocumento': None,
                'tipoPersona': None,
                'codDepto': None,
                'codMuni': None,
                'correo': None
            }
        
        # Calcular totales
        sumas = float(liquidacion.total)
        iva = 0.00  # Ajustar si manejan IVA
        total = sumas + iva
        
        # Preparar datos del encabezado
        # Convertir fecha si es necesario
        if isinstance(liquidacion.fecha, str):
            fecha_formateada = liquidacion.fecha
        else:
            fecha_formateada = liquidacion.fecha.strftime('%Y-%m-%d %H:%M:%S')
        
        prefactura_data = {
            'fecha': fecha_formateada,
            'numero': str(liquidacion.referencia),
            'codigo': str(liquidacion.cliente_id),
            'nombre': cliente.get('nombre', '')[:150],
            'direccion': cliente.get('direccion', '')[:150] if cliente.get('direccion') else None,
            'tipofactura': 'FACTURA',
            'tipoventa': 'CONTADO',
            'nregistro': cliente.get('nregistro'),
            'dui': cliente.get('dui'),
            'nit': cliente.get('nit'),
            'giro': cliente.get('giro'),
            'sumas': sumas,
            'iva': iva,
            'totalretencion': 0.00,
            'totalrenta': 0.00,
            'total': total,
            'totalnosujeta': 0.00,
            'idsucursal': '10',  # Campo idsucursal SÍ existe en prefactura
            'idusuario': None,
            'guardado': 1,  # True
            'facturado': 0,  # False - para que lo facturen
            'telefono': cliente.get('telefono'),
            'tipocliente': cliente.get('tipocliente'),
            'reserva': None,
            'caja': None,
            'codActividad': cliente.get('codActividad'),
            'tipoDocumento': cliente.get('tipoDocumento'),
            'tipoPersona': cliente.get('tipoPersona'),
            'codIncoterms': None,
            'codDepto': cliente.get('codDepto'),
            'codMuni': cliente.get('codMuni'),
            'correo': cliente.get('correo'),
            'exenta': 0,
            'retencion': 0,
            'renta': 0,
            'referencia': str(liquidacion.referencia)
        }
        
        # Insertar en prefactura
        prefactura_id = insertar_encabezado_prefactura(prefactura_data)
        
        if not prefactura_id:
            return False, "Error al insertar encabezado de prefactura", None
        
        # Insertar detalles
        detalles = liquidacion.detalles.all()
        detalles_insertados = 0
        
        for detalle in detalles:
            if detalle.cantidad_vendida > 0:  # Solo productos vendidos
                detalle_data = {
                    'idprefactura': prefactura_id,
                    'idproducto': int(detalle.producto_id),  # int - cambio ERP SIA empresa=10
                    'bodega': '10 ',  # nchar(3) - sucursal 10
                    'cantidad': float(detalle.cantidad_vendida),
                    'tipoprecio': 'PRECIO1        ',  # nchar(15)
                    'precio': float(detalle.precio),
                    'nivel': None,
                    'estante': None,
                    'averia': 0,
                    'precionuevo': None,
                    'fechaingreso': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'nomPro': obtener_nombre_producto(detalle.producto_id),
                    'caja': None,
                    'nosujeta': 0,
                    'precions': None
                }
                
                if insertar_detalle_prefactura(detalle_data):
                    detalles_insertados += 1
        
        if detalles_insertados == 0:
            return False, "No se insertaron detalles en prefactura", prefactura_id
        
        logger.info(f"✅ Prefactura {prefactura_id} creada en RQ para liquidación {liquidacion.id}")
        return True, f"Prefactura {prefactura_id} creada exitosamente con {detalles_insertados} productos", prefactura_id
        
    except Exception as e:
        logger.error(f"❌ Error al insertar prefactura en RQ: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error: {str(e)}", None


def insertar_encabezado_prefactura(data):
    """
    Inserta el encabezado en la tabla prefactura de RQ
    
    Returns:
        int: ID de la prefactura insertada o None si falla
    """
    try:
        # Función auxiliar para escapar valores SQL
        def sql_escape(value):
            if value is None:
                return 'NULL'
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, bool):
                return '1' if value else '0'
            else:
                # Escapar comillas simples
                return "'" + str(value).replace("'", "''") + "'"
        
        with connections['rq'].cursor() as cursor:
            # Construir SQL con valores directos
            sql = f"""
                INSERT INTO [dbo].[prefactura] (
                    fecha, numero, codigo, nombre, direccion, tipofactura, tipoventa,
                    nregistro, dui, nit, giro, sumas, iva, totalretencion, totalrenta,
                    total, totalnosujeta, idsucursal, idusuario, guardado, facturado,
                    telefono, tipocliente, reserva, caja, codActividad, tipoDocumento,
                    tipoPersona, codIncoterms, codDepto, codMuni, correo, exenta,
                    retencion, renta, referencia
                )
                VALUES (
                    {sql_escape(data['fecha'])}, {sql_escape(data['numero'])}, 
                    {sql_escape(data['codigo'])}, {sql_escape(data['nombre'])},
                    {sql_escape(data['direccion'])}, {sql_escape(data['tipofactura'])}, 
                    {sql_escape(data['tipoventa'])}, {sql_escape(data['nregistro'])}, 
                    {sql_escape(data['dui'])}, {sql_escape(data['nit'])}, 
                    {sql_escape(data['giro'])}, {sql_escape(data['sumas'])}, 
                    {sql_escape(data['iva'])}, {sql_escape(data['totalretencion'])}, 
                    {sql_escape(data['totalrenta'])}, {sql_escape(data['total'])}, 
                    {sql_escape(data['totalnosujeta'])}, {sql_escape(data['idsucursal'])},
                    {sql_escape(data['idusuario'])}, {sql_escape(data['guardado'])}, 
                    {sql_escape(data['facturado'])}, {sql_escape(data['telefono'])}, 
                    {sql_escape(data['tipocliente'])}, {sql_escape(data['reserva'])}, 
                    {sql_escape(data['caja'])}, {sql_escape(data['codActividad'])}, 
                    {sql_escape(data['tipoDocumento'])}, {sql_escape(data['tipoPersona'])},
                    {sql_escape(data['codIncoterms'])}, {sql_escape(data['codDepto'])}, 
                    {sql_escape(data['codMuni'])}, {sql_escape(data['correo'])},
                    {sql_escape(data['exenta'])}, {sql_escape(data['retencion'])}, 
                    {sql_escape(data['renta'])}, {sql_escape(data['referencia'])}
                )
            """
            
            cursor.execute(sql)
            
            # Obtener el ID insertado
            cursor.execute("SELECT @@IDENTITY AS id")
            result = cursor.fetchone()
            return int(result[0]) if result else None
            
    except Exception as e:
        logger.error(f"❌ Error al insertar encabezado prefactura: {e}")
        import traceback
        traceback.print_exc()
        return None


def insertar_detalle_prefactura(data):
    """
    Inserta un detalle en la tabla prefactura_detalle de RQ
    
    Returns:
        bool: True si se insertó correctamente
    """
    try:
        # Función auxiliar para escapar valores SQL
        def sql_escape(value):
            if value is None:
                return 'NULL'
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, bool):
                return '1' if value else '0'
            else:
                # Escapar comillas simples
                return "'" + str(value).replace("'", "''") + "'"
        
        with connections['rq'].cursor() as cursor:
            sql = f"""
                INSERT INTO [dbo].[prefactura_detalle] (
                    idprefactura, idproducto, bodega, cantidad, tipoprecio, precio,
                    nivel, estante, averia, precionuevo, fechaingreso, nomPro,
                    caja, nosujeta, precions
                )
                VALUES (
                    {sql_escape(data['idprefactura'])}, {sql_escape(data['idproducto'])}, 
                    {sql_escape(data['bodega'])}, {sql_escape(data['cantidad'])}, 
                    {sql_escape(data['tipoprecio'])}, {sql_escape(data['precio'])},
                    {sql_escape(data['nivel'])}, {sql_escape(data['estante'])}, 
                    {sql_escape(data['averia'])}, {sql_escape(data['precionuevo'])}, 
                    {sql_escape(data['fechaingreso'])}, {sql_escape(data['nomPro'])},
                    {sql_escape(data['caja'])}, {sql_escape(data['nosujeta'])}, 
                    {sql_escape(data['precions'])}
                )
            """
            
            cursor.execute(sql)
            return True
            
    except Exception as e:
        logger.error(f"❌ Error al insertar detalle prefactura: {e}")
        import traceback
        traceback.print_exc()
        return False


def obtener_cliente_rq(codigo_cliente):
    """
    Obtiene los datos del cliente desde la base RQ
    
    Returns:
        dict: Datos del cliente o None
    """
    try:
        with connections['rq'].cursor() as cursor:
            # Consulta con los campos reales de la tabla clientes
            sql = """
                SELECT TOP 1
                    codigo, nombre, direccion, registro, dui, nit, giro,
                    telefono, tipocliente, codActividad, codDepto, codMuni, correo
                FROM [dbo].[clientes]
                WHERE codigo = %s AND empresa = 10
            """
            
            cursor.execute(sql, (int(codigo_cliente),))
            row = cursor.fetchone()
            
            if row:
                return {
                    'codigo': row[0],
                    'nombre': row[1],
                    'direccion': row[2],
                    'nregistro': row[3],  # campo 'registro' en RQ
                    'dui': row[4],
                    'nit': row[5],
                    'giro': row[6],
                    'telefono': row[7],
                    'tipocliente': row[8],
                    'codActividad': row[9],
                    'tipoDocumento': None,  # No existe en RQ
                    'tipoPersona': None,    # No existe en RQ
                    'codDepto': row[10],
                    'codMuni': row[11],
                    'correo': row[12]
                }
            return None
            
    except Exception as e:
        logger.error(f"❌ Error al obtener cliente de RQ: {e}")
        return None


def obtener_nombre_producto(producto_id):
    """
    Obtiene el nombre del producto desde RQ
    
    Returns:
        str: Nombre del producto
    """
    try:
        with connections['rq'].cursor() as cursor:
            sql = """
                SELECT TOP 1 nombre
                FROM [dbo].[productos]
                WHERE orden = %s
            """
            
            cursor.execute(sql, (int(producto_id),))
            row = cursor.fetchone()
            
            return row[0][:1000] if row else f"Producto {producto_id}"
            
    except Exception as e:
        logger.error(f"❌ Error al obtener nombre producto: {e}")
        return f"Producto {producto_id}"
