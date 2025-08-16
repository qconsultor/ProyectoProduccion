# En produccion/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RequisicionDetalle, Producto, Kardex , CorteDeBobinaDetalle , NotaIngresoDetalle

@receiver(post_save, sender=RequisicionDetalle)
def actualizar_kardex_por_requisicion(sender, instance, created, **kwargs):
    if created:
        try:
            # Obtenemos el objeto Producto completo
            producto_encontrado = Producto.objects.using('rq').get(
                codigo=instance.producto_solicitado, 
                idsucursal=10
            )

            saldo_anterior = producto_encontrado.cantidad
            nuevo_saldo = saldo_anterior - instance.cantidad

            # Creamos el registro en Kardex con la lógica corregida
            Kardex.objects.using('rq').create(
                # 1. Aquí guardamos la RELACIÓN. Django sabe que debe usar la llave primaria de producto_encontrado (el campo 'orden')
                #    y guardarla en la columna 'regi_orden' de la tabla kardex.
                producto=producto_encontrado,

                # 2. Aquí guardamos la COPIA del código de texto.
                codigo=producto_encontrado.codigo,

                documento=f"Requisición N° {instance.requisicion.numero_requisicion}",
                # --- LÍNEA AÑADIDA ---
                descripcion=producto_encontrado.nombre,
                salida=instance.cantidad,
                saldo=nuevo_saldo,
                idsucursal=10
            )

            # Actualizamos la existencia
            producto_encontrado.cantidad = nuevo_saldo
            producto_encontrado.save(using='rq')

        except Producto.DoesNotExist:
            print(f"ADVERTENCIA: El producto con Código '{instance.producto_solicitado}' y sucursal 10 no fue encontrado.")

# Al final de produccion/signals.py

@receiver(post_save, sender=CorteDeBobinaDetalle)
def actualizar_kardex_por_corte(sender, instance, created, **kwargs):
    if created:
        # Asumimos que el 'codigo_bobina' es el SKU del producto "bobina" (materia prima)
        # Y que la descripción del reporte principal nos dice qué nuevo producto se crea.

        # --- Movimiento de SALIDA de la materia prima ---
        try:
            materia_prima = Producto.objects.using('rq').get(
                codigo=instance.codigo_bobina,
                idsucursal=10 
            )

            saldo_anterior_mp = materia_prima.cantidad
            nuevo_saldo_mp = saldo_anterior_mp - instance.resmas # Asumimos que la cantidad de salida se mide en resmas

            Kardex.objects.using('rq').create(
                producto=materia_prima,
                documento=f"Corte N° {instance.corte_de_bobina.numero_reporte}",
                # --- LÍNEA AÑADIDA ---
                descripcion=producto_terminado.nombre,
                salida=instance.resmas,
                saldo=nuevo_saldo_mp,
                idsucursal=10
            )

            materia_prima.cantidad = nuevo_saldo_mp
            materia_prima.save(using='rq')

        except Producto.DoesNotExist:
            print(f"ADVERTENCIA: Materia prima con Código '{instance.codigo_bobina}' no encontrada.")

        # --- Movimiento de ENTRADA del producto procesado ---
        # Asumimos que el 'medida_de_corte' nos da una pista del nuevo producto
        try:
            # Aquí necesitaríamos una lógica para identificar el SKU del nuevo producto (los pliegos)
            # Por ahora, vamos a simularlo buscando un producto con un SKU específico.
            # En el futuro, podrías tener un campo en el formulario que te diga qué nuevo SKU se está creando.
            producto_procesado = Producto.objects.using('rq').get(
                codigo=f"PLIEGOS-{instance.corte_de_bobina.medida_de_corte}", 
                idsucursal=10
            )

            saldo_anterior_pp = producto_procesado.cantidad
            nuevo_saldo_pp = saldo_anterior_pp + instance.pliegos # La cantidad de entrada son los pliegos

            Kardex.objects.using('rq').create(
                producto=producto_procesado,
                documento=f"Corte N° {instance.corte_de_bobina.numero_reporte}",
                # --- LÍNEA AÑADIDA ---
                descripcion=producto_terminado.nombre,
                entrada=instance.pliegos,
                saldo=nuevo_saldo_pp,
                idsucursal=10
            )

            producto_procesado.cantidad = nuevo_saldo_pp
            producto_procesado.save(using='rq')

        except Producto.DoesNotExist:
            print(f"ADVERTENCIA: Producto procesado para corte '{instance.corte_de_bobina.medida_de_corte}' no encontrado.")

###05072025

# En produccion/signals.py

@receiver(post_save, sender=NotaIngresoDetalle)
def actualizar_kardex_por_ingreso(sender, instance, created, **kwargs):
    if created:
        try:
            producto_terminado = Producto.objects.using('rq').filter(
                codigo=instance.codigo,
                idsucursal=10
            ).first()

            if producto_terminado:
                # --- LÍNEAS DE DIAGNÓSTICO (AGREGA ESTO) ---
                print("--- INICIANDO DEPURACIÓN DE SEÑAL (NOTA DE INGRESO) ---")
                print(f"Producto encontrado: {producto_terminado.nombre}")
                print(f"Código del producto a copiar: '{producto_terminado.codigo}'")
                print("--- FIN DE DEPURACIÓN ---")
                # --- FIN DE LÍNEAS DE DIAGNÓSTICO ---

                saldo_anterior = producto_terminado.cantidad
                nuevo_saldo = saldo_anterior + instance.unidades

                Kardex.objects.using('rq').create(
                    producto=producto_terminado,
                    codigo=producto_terminado.codigo, # La línea que estamos depurando
                    documento=f"Nota de Ingreso N° {instance.nota_ingreso.numero_nota}",
                    # --- LÍNEA AÑADIDA ---
                    descripcion=producto_terminado.nombre,
                    entrada=instance.unidades,
                    saldo=nuevo_saldo,
                    idsucursal=10
                )

                producto_terminado.cantidad = nuevo_saldo
                producto_terminado.save(using='rq')
            else:
                print(f"ADVERTENCIA: Producto terminado con Código '{instance.codigo}' y sucursal 10 no fue encontrado.")
        except Exception as e:
            print(f"ERROR en la señal de Nota de Ingreso: {e}")