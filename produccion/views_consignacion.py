from .forms_consignacion_detalle import ConsignacionDetalleFormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Max, Func, IntegerField, F,Sum
from django.db import transaction
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Cliente, Consignacion, ConsignacionDetalle, Producto
from .forms import ConsignacionForm, DetalleConsignacionFormSet,ConsignacionDetalleForm 
from datetime import date
from produccion.utils import get_cliente_rq   # 👈 IMPORTANTE: importas tu helper aquí

# ==============================================================================
# VISTAS PARA CLIENTES (Desde la BD 'RQ')
# ==============================================================================

def lista_clientes(request):
    clientes = Cliente.objects.using('rq').filter(empresa=10)
    return render(request, 'produccion/consignacion/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    messages.info(request, "La creación de clientes se debe realizar desde el sistema principal.")
    return redirect('produccion:lista_clientes')

def editar_cliente(request, pk):
    messages.info(request, "La edición de clientes se debe realizar desde el sistema principal.")
    return redirect('produccion:lista_clientes')

def eliminar_cliente(request, pk):
    messages.error(request, "La eliminación de clientes no está permitida desde este sistema.")
    return redirect('produccion:lista_clientes')

# ==============================================================================
# VISTAS PARA CONSIGNACIONES (LÓGICA CORREGIDA)
# ==============================================================================

def lista_consignaciones(request):
    # 1. Obtenemos todas las consignaciones de la base de datos 'default' (Personal)
    consignaciones_qs = Consignacion.objects.all().order_by('-fecha', '-id')

    # 2. Sacamos la lista de todos los IDs de clientes que necesitamos
    cliente_ids = [c.cliente_id for c in consignaciones_qs]

    # 3. Vamos a la base de datos 'rq' y traemos solo los clientes que están en esa lista
    clientes_rq = Cliente.objects.using('rq').filter(codigo__in=cliente_ids)
    
    # 4. Creamos un "diccionario" para encontrarlos fácilmente
    clientes_map = {cliente.codigo: cliente for cliente in clientes_rq}

    # 5. Unimos la información: a cada consignación le asignamos su cliente del diccionario
    for consignacion in consignaciones_qs:
        consignacion.cliente = clientes_map.get(consignacion.cliente_id)

    return render(request, 'produccion/consignacion/lista_consignaciones.html', {'consignaciones': consignaciones_qs})

def crear_consignacion(request):
    titulo = "Nueva Consignación"

    if request.method == 'POST':
        print("="*10, "DATOS POST RECIBIDOS", "="*10)
        print(request.POST)
        print("="*40)

        form = ConsignacionForm(request.POST)
        formset = DetalleConsignacionFormSet(request.POST or None, prefix='detalles')
        print('🧾 POST recibido:')
        print(request.POST)
        #print('🗑️ Objetos marcados para eliminar:', formset.deleted_objects)
        if form.is_valid() and formset.is_valid():
            try:
                consignacion = form.save(commit=False)

                # 🧭 Validar cliente con filtro empresa
                cliente_codigo = (
                    form.cleaned_data.get('cliente').codigo
                    if form.cleaned_data.get('cliente')
                    else None
                )
                cliente_obj = get_cliente_rq(cliente_codigo)

                if not cliente_obj:
                    messages.error(request, "Debes seleccionar un cliente válido (empresa 10).")
                    context = {'form': form, 'formset': formset, 'titulo': titulo}
                    return render(request, 'produccion/consignacion/consignacion_form.html', context)

                consignacion.cliente = cliente_obj

                # 🧮 Recalcular referencia por seguridad antes de guardar
                max_ref = Consignacion.objects.annotate(
                    ref_int=Func(F('referencia'), function='CAST', template='CAST(%(expressions)s AS INT)')
                ).aggregate(max_referencia=Max('ref_int'))['max_referencia'] or 0
                consignacion.referencia = str(max_ref + 1)

                # 🧾 Calcular totales de los detalles
                total_consignacion = 0
                detalles_para_guardar = []

                for form_detalle in formset:
                    if form_detalle.cleaned_data and form_detalle.has_changed() and not form_detalle.cleaned_data.get('DELETE', False):
                        detalle = form_detalle.save(commit=False)
                        cantidad = form_detalle.cleaned_data.get('cantidad', 0) or 0
                        precio = form_detalle.cleaned_data.get('precio', 0) or 0
                        detalle.total_linea = cantidad * precio
                        total_consignacion += detalle.total_linea
                        detalles_para_guardar.append(detalle)

                if not detalles_para_guardar:
                    messages.warning(request, "Debes añadir al menos un producto a la consignación.")
                    context = {'form': form, 'formset': formset, 'titulo': titulo}
                    return render(request, 'produccion/consignacion/consignacion_form.html', context)

                consignacion.total = total_consignacion

                # 🧠 Intentar guardar — si hay error por duplicado recalcular automáticamente
                try:
                    consignacion.save(using='default')
                except Exception as e:
                    if 'UQ_produccion_consignacion_referencia' in str(e):
                        print(f"⚠️ Referencia duplicada detectada ({consignacion.referencia}). Recalculando...")
                        max_ref2 = Consignacion.objects.annotate(
                            ref_int=Func(F('referencia'), function='CAST', template='CAST(%(expressions)s AS INT)')
                        ).aggregate(max_referencia=Max('ref_int'))['max_referencia'] or 0
                        consignacion.referencia = str(max_ref2 + 1)
                        consignacion.save(using='default')
                    else:
                        raise

                # 💾 Guardar los detalles
                for detalle in detalles_para_guardar:
                    detalle.consignacion = consignacion
                    detalle.save(using='default')

                messages.success(request, f"✅ ¡Consignación #{consignacion.referencia} guardada con éxito!")
                return redirect('produccion:lista_consignaciones')

            except Exception as e:
                messages.error(request, f"Error al guardar la consignación: {e}")
                print(f"Error al guardar: {e}")


    else:
        # --- BLOQUE GET ---
        try:
            # ultimo_numero_str = Consignacion.objects.using('default').aggregate(
            #     max_referencia=Max('referencia')
            # )['max_referencia']
            # Si referencia es texto, la convertimos a entero para evitar que '9' > '10'
            ultimo_numero_str = Consignacion.objects.using('default').annotate(
                ref_int=Func(F('referencia'), function='CAST', template='CAST(%(expressions)s AS INT)')
            ).aggregate(
                max_referencia=Max('ref_int')
            )['max_referencia']
            print("🔹 Última referencia encontrada:", ultimo_numero_str)

            ultimo_numero = int(ultimo_numero_str) if ultimo_numero_str else 0
            siguiente_numero = ultimo_numero + 1
        except Exception as e:
            print(f"⚠️ Error al calcular la referencia: {e}")
            siguiente_numero = 1

        form = ConsignacionForm(initial={
            'referencia': siguiente_numero,
            'fecha': date.today()
        })
        formset = DetalleConsignacionFormSet(prefix='detalles')

    context = {
        'form': form,
        'formset': formset,
        'titulo': titulo,
    }
    return render(request, 'produccion/consignacion/consignacion_form.html', context)


def editar_consignacion(request, pk):
    consignacion = get_object_or_404(Consignacion, pk=pk)
    
    # 🔹 Filtro correcto de cliente según empresa
    cliente = None
    if consignacion.cliente_id:
        cliente = Cliente.objects.using('rq').filter(
            codigo=consignacion.cliente_id, empresa=10
        ).first()
    DetalleFormSet = modelformset_factory(
        ConsignacionDetalle,
        form=ConsignacionDetalleForm,
        extra=1,
        can_delete=True,
        validate_max=False,
        validate_min=False
    )

    # DetalleFormSet = modelformset_factory(
    #     ConsignacionDetalle,
    #     form=ConsignacionDetalleForm,
    #     extra=1,
    #     can_delete=True
    # )

    if request.method == 'POST':
        form = ConsignacionForm(request.POST, instance=consignacion)
        formset = DetalleFormSet(
            request.POST,
            queryset=ConsignacionDetalle.objects.filter(consignacion=consignacion),
            prefix='detalles'
        )
        if form.is_valid() and formset.is_valid():
            consignacion = form.save(commit=False)
            consignacion.save()

            total_general = 0
            detalles = formset.save(commit=False)

            # 🔹 Guardar detalles
            for detalle in detalles:
                detalle.consignacion = consignacion
                detalle.total_linea = (detalle.cantidad or 0) * (detalle.precio or 0)
                detalle.save()
                total_general += detalle.total_linea

            # 🔹 Eliminar los marcados como DELETE
            #for obj in formset.deleted_objects:
            #    obj.delete()
            # ✅ ahora
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()


            # 🔹 Actualizar total de la consignación
            consignacion.total = total_general
            consignacion.save()

            messages.success(request, f'Consignación #{consignacion.referencia} actualizada correctamente.')
            return redirect('consignacion:lista_consignaciones')

        else:
            print('⚠️ Formulario inválido:', form.errors, formset.errors)

    else:
        form = ConsignacionForm(instance=consignacion)
        
        # 🔹 Crear el formset primero
        formset = DetalleFormSet(
            queryset=ConsignacionDetalle.objects.filter(consignacion=consignacion),
            prefix='detalles'
        )
        
        # 🔹 Pre-cargar los productos desde la BD 'rq' manualmente
        producto_ids = []
        for form_detalle in formset:
            if hasattr(form_detalle.instance, 'producto_id') and form_detalle.instance.producto_id:
                # Convertir a int por si acaso viene como string
                try:
                    pid = int(form_detalle.instance.producto_id)
                    producto_ids.append(pid)
                except (ValueError, TypeError):
                    print(f"⚠️ Error convirtiendo producto_id: {form_detalle.instance.producto_id}")
        
        # 🔹 Obtener todos los productos en una sola query
        if producto_ids:
            productos_dict = {
                p.orden: p for p in Producto.objects.using('rq').filter(orden__in=producto_ids)
            }
        else:
            productos_dict = {}
        
        # 🔹 Asignar los productos a cada formulario del formset
        for form_detalle in formset:
            if hasattr(form_detalle.instance, 'producto_id') and form_detalle.instance.producto_id:
                try:
                    pid = int(form_detalle.instance.producto_id)
                    producto_obj = productos_dict.get(pid)
                    form_detalle.instance.producto_obj = producto_obj
                except (ValueError, TypeError) as e:
                    print(f"⚠️ Error procesando detalle: {e}")

    context = {
        'form': form,
        'formset': formset,
        'titulo': f'Editar Consignación #{consignacion.referencia}',
        'cliente_obj': cliente,  # 👈 Esto rellena el select2 del cliente
    }
    return render(request, 'produccion/consignacion/consignacion_form.html', context)

def detalle_consignacion(request, pk):
    consignacion = get_object_or_404(
        Consignacion.objects.prefetch_related('detalles', 'detalles__producto'),
        pk=pk
    )

    # 🔒 Traer el cliente solo de empresa 10 para evitar duplicados
    cliente = (
        Cliente.objects.using('rq')
        .filter(empresa=10, codigo=consignacion.cliente_id)
        .first()
    )

    # 🔸 Si no se encuentra el cliente, mostramos un mensaje o texto por defecto
    consignacion.cliente_obj = cliente or None

    return render(
        request,
        'produccion/consignacion/detalle_consignacion.html',
        {
            'consignacion': consignacion,
            'cliente_nombre': cliente.nombre if cliente else '(Cliente no encontrado)'
        }
    )

def eliminar_consignacion(request, pk):
    Cliente.objects.get
    consignacion = get_object_or_404(Consignacion, pk=pk)
    if request.method == 'POST':
        consignacion.delete()
        messages.success(request, f"Consignación #{consignacion.id} eliminada.")
        return redirect('produccion:lista_consignaciones')
    return render(request, 'produccion/consignacion/eliminar_consignacion.html', {'consignacion': consignacion})

def registrar_devolucion(request, consignacion_id):
    messages.info(request, "Funcionalidad de devoluciones en construcción.")
    return redirect('produccion:detalle_consignacion', pk=consignacion_id)
# ===============================
# 🧩 FormSet personalizado
# ===============================
from django.forms import BaseInlineFormSet

class ConsignacionDetalleBaseFormSet(BaseInlineFormSet):
    def clean(self):
        """Ignora formularios vacíos para evitar el error 'This field is required'."""
        super().clean()
        for form in self.forms:
            # Si el formulario está vacío, no genera error
            if not form.cleaned_data:
                continue

            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad')
            precio = form.cleaned_data.get('precio')

            # Si tiene cantidad o precio pero no producto → error
            if not producto and (cantidad or precio):
                form.add_error('producto', 'Debe seleccionar un producto.')
# ==============================================================================
# APIs para los buscadores (CON FILTROS AÑADIDOS)
# ==============================================================================

def buscar_clientes_api(request):
    query = request.GET.get('term', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    clientes = Cliente.objects.using('rq').filter(
        (Q(nombre__icontains=query) | Q(codigo__icontains=query)) &
        Q(empresa=10) 
    )[:20]
    
    #results = [{'id': c.codigo, 'text': f"{c.nombre} ({c.codigo})"} for c in clientes]
    #return JsonResponse({'results': results})
    # ✅ Aquí el cambio importante: usamos c.id en vez de c.codigo
    # ✅ Usamos c.codigo, que es la PK real de clientes
    results = [{'id': c.codigo, 'text': f"{c.nombre} ({c.codigo})"} for c in clientes]
    return JsonResponse({'results': results})

def buscar_productos_consignacion_api(request):
    term = request.GET.get('term', '')
    
    # 🔹 Filtrar productos EXCLUYENDO bobinas, químicos y tintas
    productos_encontrados = Producto.objects.using('rq').filter(
        Q(codigo__icontains=term) | Q(nombre__icontains=term),
        idsucursal=10 
    ).exclude(
        Q(nombre__icontains='BOBINA') | 
        Q(nombre__icontains='QUIMICO') | 
        Q(nombre__icontains='TINTA')
    ).order_by('nombre')[:15]

    resultados = []
    for producto in productos_encontrados:
        resultados.append({
            'id': producto.orden,  # Usamos la PK 'orden' (un número)
            'text': f"{producto.codigo} | {producto.nombre}",
            'precio': float(producto.venta),  # Precio de venta
            'existencia': float(producto.cantidad)  # Stock disponible
        })
    
    return JsonResponse({'results': resultados}, safe=False)



# --- NUEVA API AÑADIDA ---
def get_producto_detalle_consignacion_api(request):
    producto_id = request.GET.get('id') # Esto ahora es un número ('orden')
    try:
        producto = Producto.objects.using('rq').get(pk=producto_id)
        
        precio_redondeado = round(producto.venta, 2)
        
        data = {
            'precio': precio_redondeado,
            'existencia': producto.cantidad
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# def get_producto_detalle_consignacion_api(request):
#     producto_id = request.GET.get('id')
#     # Busca en la base de datos 'rq' y usa 'codigo' en lugar de 'pk'
#     producto = Producto.objects.using('rq').get(codigo=producto_id) # <-- ¡SOLUCIÓN!
#     try:
#         # Buscamos el producto por su código (que es la llave primaria)
#         producto = Producto.objects.get(pk=producto_id)
#         data = {
#             'venta': producto.venta,
#             'existencia': producto.cantidad
#         }
#         return JsonResponse(data)
#     except Producto.DoesNotExist:
#         return JsonResponse({'error': 'Producto no encontrado'}, status=404)
# -------------------------
