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
        documento_ref = f"Reporte de Corte N° {instance.corte_de_bobina.numero_reporte}"

        # --- ¡NUEVO BLOQUE TRY...EXCEPT PARA CAPTURAR TODO! ---
        try:
            # --- Lógica de SALIDA de la bobina usada ---
            try:
                bobina_usada = Producto.objects.using('rq').get(codigo=instance.codigo_bobina_usada, idsucursal=10)
                saldo_anterior = bobina_usada.cantidad
                nuevo_saldo = saldo_anterior - 1
                
                # Revisa los campos de tu tabla Kardex.
                # Si te faltan campos NOT NULL, añádelos aquí con valores por defecto
                Kardex.objects.using('rq').create(
                    producto=bobina_usada, 
                    codigo=bobina_usada.codigo,
                    descripcion=bobina_usada.nombre, 
                    documento=documento_ref,
                    salida=1, 
                    saldo=nuevo_saldo, 
                    idsucursal=10
                    # ¿Falta 'lote', 'usuario', 'tipo', etc.?
                )
                
                bobina_usada.cantidad = nuevo_saldo
                bobina_usada.save(using='rq')
            except Producto.DoesNotExist:
                print(f"ERROR en KARDEX: Bobina con código '{instance.codigo_bobina_usada}' no encontrada.")

            # --- Lógica de ENTRADA para el Pliego 1 ---
            if instance.codigo_pliego_producido_1 and instance.cantidad_pliegos_1 > 0:
                try:
                    pliego1 = Producto.objects.using('rq').get(codigo=instance.codigo_pliego_producido_1, idsucursal=10)
                    saldo_anterior_p1 = pliego1.cantidad
                    nuevo_saldo_p1 = saldo_anterior_p1 + instance.cantidad_pliegos_1
                    Kardex.objects.using('rq').create(
                        producto=pliego1, 
                        codigo=pliego1.codigo,
                        descripcion=pliego1.nombre, 
                        documento=documento_ref,
                        entrada=instance.cantidad_pliegos_1, 
                        saldo=nuevo_saldo_p1, 
                        idsucursal=10
                    )
                    pliego1.cantidad = nuevo_saldo_p1
                    pliego1.save(using='rq')
                except Producto.DoesNotExist:
                    print(f"ERROR en KARDEX: Pliego 1 con código '{instance.codigo_pliego_producido_1}' no encontrado.")

            # --- Lógica de ENTRADA para el Pliego 2 (si existe) ---
            if instance.codigo_pliego_producido_2 and instance.cantidad_pliegos_2 > 0:
                try:
                    pliego2 = Producto.objects.using('rq').get(codigo=instance.codigo_pliego_producido_2, idsucursal=10)
                    saldo_anterior_p2 = pliego2.cantidad
                    nuevo_saldo_p2 = saldo_anterior_p2 + instance.cantidad_pliegos_2
                    Kardex.objects.using('rq').create(
                        producto=pliego2, 
                        codigo=pliego2.codigo,
                        descripcion=pliego2.nombre, 
                        documento=documento_ref,
                        entrada=instance.cantidad_pliegos_2, 
                        saldo=nuevo_saldo_p2, 
                        idsucursal=10
                    )
                    pliego2.cantidad = nuevo_saldo_p2
                    pliego2.save(using='rq')
                except Producto.DoesNotExist:
                    print(f"ERROR en KARDEX: Pliego 2 con código '{instance.codigo_pliego_producido_2}' no encontrado.")
        
        except Exception as e:
            # ¡¡ESTO CAPTURARÁ EL VERDADERO ERROR!!
            print("="*40)
            print(f"¡¡ERROR GENERAL EN LA SEÑAL DE CORTE!!: {e}")
            print(f"Instancia: {instance.__dict__}")
            print("="*40)



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