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

# En produccion/signals.py

@receiver(post_save, sender=CorteDeBobinaDetalle)
def actualizar_kardex_por_corte(sender, instance, created, **kwargs):
    """
    Esta señal se dispara cuando se guarda un detalle de corte.
    Su propósito es registrar la SALIDA de la bobina utilizada.
    """
    if created:
        try:
            # 1. Buscamos la bobina (materia prima) que se usó.
            bobina_utilizada = Producto.objects.using('rq').get(
                codigo=instance.codigo_bobina,
                idsucursal=10 
            )

            # 2. Calculamos el nuevo saldo (descontamos 1 unidad).
            saldo_anterior = bobina_utilizada.cantidad
            nuevo_saldo = saldo_anterior - 1 # Descontamos una bobina

            # 3. Creamos el registro de SALIDA en el Kardex.
            Kardex.objects.using('rq').create(
                producto=bobina_utilizada,
                codigo=bobina_utilizada.codigo,
                # Usamos el nombre del producto en la descripción del movimiento
                descripcion=bobina_utilizada.nombre, 
                documento=f"Reporte de Corte N° {instance.corte_de_bobina.numero_reporte}",
                salida=1, # La salida es de 1 unidad (una bobina)
                saldo=nuevo_saldo,
                idsucursal=10
            )

            # 4. Actualizamos la existencia total del producto.
            bobina_utilizada.cantidad = nuevo_saldo
            bobina_utilizada.save(using='rq')

        except Producto.DoesNotExist:
            print(f"ADVERTENCIA: La bobina con Código '{instance.codigo_bobina}' no fue encontrada en el catálogo.")
        except Exception as e:
            print(f"ERROR inesperado en la señal de corte de bobina: {e}")

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