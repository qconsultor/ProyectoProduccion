from xml.dom.minidom import Document
from django.db import transaction
from django.utils import timezone
import decimal
# Al principio de produccion/views.py
from datetime import date
from django.db.models import Q
from django.db.models.functions import Trim
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory,modelformset_factory # <-- ¡AÑADE ESTA LÍNEA!
from django.contrib import messages
from django.http import JsonResponse
# Al principio de produccion/views.py
from .models import (
    OrdenProduccion, RequisicionEncabezado, ControlProceso, CorteDeBobina, CorteDeBobinaDetalle, 
    ReporteDiarioProductoTerminado, NotaIngresoProductoTerminado, 
    Producto, Kardex,
    ControlProcesoDetalle # <-- AÑADE ESTA LÍNEA QUE FALTABA
)
#from .forms import OrdenProduccionForm, RequisicionForm
from .forms import OrdenProduccionForm, RequisicionForm, ControlProcesoForm , ReporteDiarioForm , NotaIngresoForm, CorteDeBobinaForm, CorteDeBobinaDetalleForm, CorteDeBobinaDetalleFormEditar,ProductoForm,ControlProcesoDetalleForm

#dashboard
# En produccion/views.py

def dashboard_produccion(request):
    # Buscamos todas las órdenes, las más nuevas primero
    ordenes = OrdenProduccion.objects.all().order_by('-id') 

    contexto = {
        'ordenes': ordenes
    }
    return render(request, 'produccion/dashboard.html', contexto)

# Create your views here. ORDENES
# En produccion/views.py

# En produccion/views.py

def lista_ordenes(request):
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    ordenes = OrdenProduccion.objects.all()

    if fecha_desde:
        # CORREGIDO: Usamos 'fecha'
        ordenes = ordenes.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        # CORREGIDO: Usamos 'fecha'
        ordenes = ordenes.filter(fecha__lte=fecha_hasta)

    contexto = {
        'ordenes': ordenes.order_by('-fecha'), # CORREGIDO: Usamos 'fecha'
        'fecha_desde_valor': fecha_desde,
        'fecha_hasta_valor': fecha_hasta,
    }
    return render(request, 'produccion/lista_ordenes.html', contexto)

# AGREGA ESTA NUEVA FUNCIÓN
def detalle_orden(request, orden_id):
    # 1. Obtener un ÚNICO objeto usando su ID (llave primaria, pk)
    orden = get_object_or_404(OrdenProduccion, pk=orden_id)

    # 2. Pasarlo al contexto
    contexto = {
        'orden': orden
    }

    # 3. Renderizar una NUEVA plantilla para los detalles
    return render(request, 'produccion/detalle_orden.html', contexto)

def crear_orden(request):
    if request.method == 'POST':
        # Si el método es POST, significa que el usuario ha enviado el formulario
        form = OrdenProduccionForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el nuevo objeto en la base de datos
            return redirect('lista_ordenes') # Redirige al usuario a la lista de órdenes
    else:
        # Si el método es GET, significa que el usuario acaba de entrar a la página
        # y le mostramos un formulario vacío.
        form = OrdenProduccionForm()

    contexto = {
        'form': form
    }
    return render(request, 'produccion/crear_orden.html', contexto)

def editar_orden(request, orden_id):
    # Primero, obtenemos la orden específica que se va a editar
    orden = get_object_or_404(OrdenProduccion, pk=orden_id)

    if request.method == 'POST':
        # Si el usuario envía el formulario, llenamos el formulario con los datos enviados
        # Y le decimos que estamos actualizando la instancia 'orden' que ya cargamos
        form = OrdenProduccionForm(request.POST, instance=orden)
        if form.is_valid():
            form.save() # Como la instancia ya existe, .save() la actualiza
            return redirect('lista_ordenes') # Volvemos a la lista
    else:
        # Si el usuario solo está visitando la página, le mostramos el formulario
        # pre-llenado con los datos de la instancia 'orden'
        form = OrdenProduccionForm(instance=orden)

    contexto = {
        'form': form
    }
    # ¡Podemos reusar la misma plantilla que para crear!
    return render(request, 'produccion/crear_orden.html', contexto)

def eliminar_orden(request, orden_id):
    # Obtenemos la orden que se va a eliminar
    orden = get_object_or_404(OrdenProduccion, pk=orden_id)

    if request.method == 'POST':
        # Si el usuario confirma (hace clic en el botón del formulario)...
        orden.delete() # ...se elimina el objeto de la base de datos
        return redirect('lista_ordenes') # Y volvemos a la lista

    # Si es la primera vez que entra (GET), solo mostramos la página de confirmación
    contexto = {
        'orden': orden
    }
    return render(request, 'produccion/eliminar_orden.html', contexto)

##### REQUISICIONES
# --- VISTAS PARA LA GESTIÓN DE REQUISICIONES ---

def lista_requisiciones(request):
    # 1. Cambiamos el modelo a RequisicionEncabezado
    requisiciones = RequisicionEncabezado.objects.all()
    # 2. Creamos el contexto
    contexto = {
        'requisiciones': requisiciones
    }
    # 3. Apuntamos a una nueva plantilla HTML
    return render(request, 'produccion/lista_requisiciones.html', contexto)

def detalle_requisicion(request, req_id):
    # Usamos el modelo correcto y el id correcto
    requisicion = get_object_or_404(RequisicionEncabezado, pk=req_id)
    contexto = {
        'requisicion': requisicion
    }
    return render(request, 'produccion/detalle_requisicion.html', contexto)

def crear_requisicion(request):
    if request.method == 'POST':
        # Usamos el formulario correcto
        form = RequisicionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_requisiciones') # Redirigimos a la lista de requisiciones
    else:
        form = RequisicionForm()

    contexto = {
        'form': form
    }
    # Apuntamos a la plantilla de creación de requisiciones
    return render(request, 'produccion/crear_requisicion.html', contexto)

def editar_requisicion(request, req_id):
    requisicion = get_object_or_404(RequisicionEncabezado, pk=req_id)
    if request.method == 'POST':
        form = RequisicionForm(request.POST, instance=requisicion)
        if form.is_valid():
            form.save()
            return redirect('lista_requisiciones')
    else:
        form = RequisicionForm(instance=requisicion)

    contexto = {
        'form': form
    }
    # Reutilizamos la plantilla de creación
    return render(request, 'produccion/crear_requisicion.html', contexto)

def eliminar_requisicion(request, req_id):
    requisicion = get_object_or_404(RequisicionEncabezado, pk=req_id)
    if request.method == 'POST':
        requisicion.delete()
        return redirect('lista_requisiciones')

    contexto = {
        'requisicion': requisicion
    }
    return render(request, 'produccion/eliminar_requisicion.html', contexto)  

### CONTROL DE PROCESOS
# --- AGREGA ESTE NUEVO BLOQUE DE VISTAS ---

def lista_controles(request):
    controles = ControlProceso.objects.all()
    contexto = {'controles': controles}
    return render(request, 'produccion/lista_controles.html', contexto)

def editar_control(request, control_id):
    control = get_object_or_404(ControlProceso, pk=control_id)

    ControlProcesoDetalleFormSet = inlineformset_factory(
        ControlProceso, 
        ControlProcesoDetalle, 
        form=ControlProcesoDetalleForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = ControlProcesoForm(request.POST, instance=control)
        formset = ControlProcesoDetalleFormSet(request.POST, instance=control)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, '¡Control de proceso actualizado exitosamente!')
            return redirect('detalle_control', control_id=control.id)
    else:
        form = ControlProcesoForm(instance=control)
        formset = ControlProcesoDetalleFormSet(instance=control)

    contexto = {
        'form': form,
        'formset': formset,
        'control': control,
    }
    return render(request, 'produccion/crear_control.html', contexto)

# --- INICIO DE LA CORRECCIÓN: AÑADIR LA FUNCIÓN QUE FALTABA ---
def detalle_control(request, control_id):
    control = get_object_or_404(ControlProceso, pk=control_id)
    
    # Buscamos todos los detalles que pertenecen a este control
    detalles_del_proceso = control.detalles.all().order_by('fecha', 'turno')

    contexto = {
        'control': control,
        'detalles': detalles_del_proceso # Pasamos los detalles a la plantilla
    }
    return render(request, 'produccion/detalle_control.html', contexto)
# --- FIN DE LA CORRECCIÓN ---

# def detalle_control(request, control_id):
#     control = get_object_or_404(ControlProceso, pk=control_id)
#     #contexto = {'control': control}
#     # --- INICIO DE LA CORRECCIÓN ---
#     # ¡LA LÍNEA QUE FALTABA! 
#     # Le decimos a Django que busque todos los detalles que pertenecen a este control.
#     detalles_del_proceso = control.detalles.all().order_by('fecha', 'turno')
#     # --- FIN DE LA CORRECCIÓN ---
#     contexto = {
#         'control': control,
#         'detalles': detalles_del_proceso # <-- Pasamos los detalles encontrados a la plantilla
#     }
#     return render(request, 'produccion/detalle_control.html', contexto)

def crear_control(request):
    if request.method == 'POST':
        form = ControlProcesoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_controles')
    else:
        form = ControlProcesoForm()
    contexto = {'form': form}
    return render(request, 'produccion/crear_control.html', contexto)
# --- REEMPLAZA ESTA FUNCIÓN ---




def eliminar_control(request, control_id):
    control = get_object_or_404(ControlProceso, pk=control_id)
    if request.method == 'POST':
        control.delete()
        return redirect('lista_controles')
    contexto = {'control': control}
    return render(request, 'produccion/eliminar_control.html', contexto) 

#, ReporteDiarioForm             
# --- AGREGA ESTE NUEVO BLOQUE DE VISTAS ---

def lista_reportes_diarios(request):
    reportes = ReporteDiarioProductoTerminado.objects.all()
    return render(request, 'produccion/lista_reportes_diarios.html', {'reportes': reportes})

def detalle_reporte_diario(request, reporte_id):
    reporte = get_object_or_404(ReporteDiarioProductoTerminado, pk=reporte_id)
    return render(request, 'produccion/detalle_reporte_diario.html', {'reporte': reporte})

def crear_reporte_diario(request):
    if request.method == 'POST':
        form = ReporteDiarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes_diarios')
    else:
        form = ReporteDiarioForm()
    return render(request, 'produccion/crear_reporte_diario.html', {'form': form})

def editar_reporte_diario(request, reporte_id):
    reporte = get_object_or_404(ReporteDiarioProductoTerminado, pk=reporte_id)
    if request.method == 'POST':
        form = ReporteDiarioForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes_diarios')
    else:
        form = ReporteDiarioForm(instance=reporte)
    return render(request, 'produccion/crear_reporte_diario.html', {'form': form, 'reporte': reporte})

def eliminar_reporte_diario(request, reporte_id):
    reporte = get_object_or_404(ReporteDiarioProductoTerminado, pk=reporte_id)
    if request.method == 'POST':
        reporte.delete()
        return redirect('lista_reportes_diarios')
    return render(request, 'produccion/eliminar_reporte_diario.html', {'reporte': reporte})

# --- AGREGA ESTE NUEVO BLOQUE DE VISTAS ---

def lista_notas_ingreso(request):
    notas = NotaIngresoProductoTerminado.objects.all()
    return render(request, 'produccion/lista_notas_ingreso.html', {'notas': notas})

def detalle_nota_ingreso(request, nota_id):
    nota = get_object_or_404(NotaIngresoProductoTerminado, pk=nota_id)
    return render(request, 'produccion/detalle_nota_ingreso.html', {'nota': nota})

def crear_nota_ingreso(request):
    if request.method == 'POST':
        form = NotaIngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_notas_ingreso')
    else:
        form = NotaIngresoForm()
    return render(request, 'produccion/crear_nota_ingreso.html', {'form': form})

def editar_nota_ingreso(request, nota_id):
    nota = get_object_or_404(NotaIngresoProductoTerminado, pk=nota_id)
    if request.method == 'POST':
        form = NotaIngresoForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('lista_notas_ingreso')
    else:
        form = NotaIngresoForm(instance=nota)
    return render(request, 'produccion/crear_nota_ingreso.html', {'form': form, 'nota': nota})

def eliminar_nota_ingreso(request, nota_id):
    nota = get_object_or_404(NotaIngresoProductoTerminado, pk=nota_id)
    if request.method == 'POST':
        nota.delete()
        return redirect('lista_notas_ingreso')
    return render(request, 'produccion/eliminar_nota_ingreso.html', {'nota': nota})

# En produccion/views.py

    

# def reporte_kardex(request):
#     codigo_buscado = request.GET.get('codigo_producto', '')
#     # --- NUEVO: Obtenemos las fechas del formulario ---
#     fecha_desde = request.GET.get('fecha_desde', '')
#     fecha_hasta = request.GET.get('fecha_hasta', '')

#     movimientos = None

#     if codigo_buscado:
#         # Empezamos filtrando por el código del producto
#         movimientos = Kardex.objects.using('rq').filter(codigo=codigo_buscado)

#         # --- NUEVO: Si hay fechas, añadimos más filtros a la consulta ---
#         if fecha_desde:
#             # __date__gte = la FECHA del campo sea "mayor o igual que"
#             movimientos = movimientos.filter(fecha__date__gte=fecha_desde)

#         if fecha_hasta:
#             # __date__lte = la FECHA del campo sea "menor o igual que"
#             movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)

#         # Ordenamos el resultado final
#         movimientos = movimientos.order_by('fecha')

#     contexto = {
#         'movimientos': movimientos,
#         'codigo_buscado': codigo_buscado,
#         # --- NUEVO: Devolvemos las fechas a la plantilla para que las "recuerde" ---
#         'fecha_desde_valor': fecha_desde,
#         'fecha_hasta_valor': fecha_hasta,
#     }
#     return render(request, 'produccion/reporte_kardex.html', contexto)
#31082025
# def reporte_kardex(request):
#     codigo_buscado = request.GET.get('codigo_producto', '')
#     fecha_desde = request.GET.get('fecha_desde', '')
#     fecha_hasta = request.GET.get('fecha_hasta', '')

#     movimientos = None

#     if codigo_buscado:
#         # --- LÍNEA CORREGIDA ---
#         # Ahora filtramos por el 'codigo' del 'producto' relacionado.
#         movimientos = Kardex.objects.using('rq').filter(producto__codigo=codigo_buscado)
#         # -------------------------

#         if fecha_desde:
#             movimientos = movimientos.filter(fecha__date__gte=fecha_desde)

#         if fecha_hasta:
#             movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)

#         # --- AÑADE ESTA LÍNEA PARA DEPURAR ---
#         print("SQL GENERADO:", movimientos.query)
#         # ------------------------------------

#         movimientos = movimientos.order_by('fecha')

#     contexto = {
#         'movimientos': movimientos,
#         'codigo_buscado': codigo_buscado,
#         'fecha_desde_valor': fecha_desde,
#         'fecha_hasta_valor': fecha_hasta,
#     }
#     return render(request, 'produccion/reporte_kardex.html', contexto)
#3108205 SEGUNDA DE ESTE DIA 

# En produccion/views.py

# En produccion/views.py

# En produccion/views.py

def reporte_kardex(request):
    codigo_buscado = request.GET.get('codigo_producto', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    movimientos = Kardex.objects.none() 

    if codigo_buscado:
        codigos_validos = set(Producto.objects.using('rq').values_list('codigo', flat=True))

        if codigo_buscado in codigos_validos:
            # Usamos TRIM para eliminar espacios en blanco del campo de la base de datos antes de comparar
            where_conditions = [
                f"TRIM(productos.codigo) = '{codigo_buscado}'"
            ]

            if fecha_desde:
                where_conditions.append(f"CAST(kardex.fecha AS date) >= '{fecha_desde}'")

            if fecha_hasta:
                where_conditions.append(f"CAST(kardex.fecha AS date) <= '{fecha_hasta}'")

            final_where_clause = " AND ".join(where_conditions)

            movimientos = Kardex.objects.using('rq').select_related('producto').extra(
                where=[final_where_clause]
            ).order_by('fecha')

    contexto = {
        'movimientos': movimientos,
        'codigo_buscado': codigo_buscado,
        'fecha_desde_valor': fecha_desde,
        'fecha_hasta_valor': fecha_hasta,
    }
    return render(request, 'produccion/reporte_kardex.html', contexto)

#31082025558pm
# PEGA ESTA FUNCIÓN DE VUELTA EN TU views.py

def reporte_kardex_imprimir(request):
    codigo_buscado = request.GET.get('codigo_producto', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    movimientos = None
    producto = None

    if codigo_buscado:
        # Usamos la misma lógica corregida de la vista principal
        movimientos = Kardex.objects.using('rq').filter(producto__codigo__exact=codigo_buscado)

        try:
            # Buscamos el objeto producto para mostrar su nombre en la impresión
            producto = Producto.objects.using('rq').get(codigo=codigo_buscado)
        except (Producto.DoesNotExist, Producto.MultipleObjectsReturned):
            producto = None

        if fecha_desde:
            movimientos = movimientos.filter(fecha__date__gte=fecha_desde)

        if fecha_hasta:
            movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)

        movimientos = movimientos.order_by('fecha')

    contexto = {
        'movimientos': movimientos,
        'producto': producto,
        'codigo_buscado': codigo_buscado,
        'fecha_desde_valor': fecha_desde,
        'fecha_hasta_valor': fecha_hasta,
    }
    return render(request, 'produccion/reporte_kardex_imprimir.html', contexto)

#17082025
# Al final de produccion/views.py
from django.http import JsonResponse



#18082025
# En produccion/views.py
# En produccion/views.py

def crear_corte(request):
    DetalleFormSet = modelformset_factory(CorteDeBobinaDetalle, form=CorteDeBobinaDetalleForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = CorteDeBobinaForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, queryset=CorteDeBobinaDetalle.objects.none())

        if form.is_valid() and detalle_formset.is_valid():
            corte_instance = form.save()
            instances = detalle_formset.save(commit=False)
            for instance in instances:
                # Solo guardamos las filas que el usuario llenó
                if hasattr(instance, 'codigo_bobina_usada') and instance.codigo_bobina_usada: 
                    instance.corte_de_bobina = corte_instance
                    instance.save()

            messages.success(request, f'¡Reporte de Corte N° {corte_instance.numero_reporte} guardado exitosamente!')
            return redirect('lista_cortes')
    else:
        # --- LÓGICA PARA VALORES POR DEFECTO ---
        try:
            # Calculamos el siguiente número de reporte
            ultimo_reporte = CorteDeBobina.objects.aggregate(max_num=Max('numero_reporte'))
            numero_maximo_texto = ultimo_reporte['max_num'] or '0'
            siguiente_numero = int(numero_maximo_texto) + 1
        except:
            siguiente_numero = 1 # Si hay un error, empezamos en 1

        # Preparamos los datos iniciales para el formulario
        initial_data = {
            'numero_reporte': siguiente_numero,
            'fecha': date.today()
        }
        form = CorteDeBobinaForm(initial=initial_data)
        detalle_formset = DetalleFormSet(queryset=CorteDeBobinaDetalle.objects.none())

    return render(request, 'produccion/crear_corte.html', {'form': form, 'detalle_formset': detalle_formset})

def editar_corte(request, corte_id):
    corte = get_object_or_404(CorteDeBobina, pk=corte_id)
    DetalleFormSet = modelformset_factory(CorteDeBobinaDetalle, form=CorteDeBobinaDetalleForm, extra=0, can_delete=True)
    if request.method == 'POST':
        form = CorteDeBobinaForm(request.POST, instance=corte)
        detalle_formset = DetalleFormSet(request.POST, queryset=CorteDeBobinaDetalle.objects.filter(corte_de_bobina=corte))
        if form.is_valid() and detalle_formset.is_valid():
            form.save()
            detalle_formset.save()
            messages.success(request, f'¡Reporte de Corte N° {corte.numero_reporte} actualizado exitosamente!')
            return redirect('lista_cortes')
    else:
        form = CorteDeBobinaForm(instance=corte)
        detalle_formset = DetalleFormSet(queryset=CorteDeBobinaDetalle.objects.filter(corte_de_bobina=corte))
    return render(request, 'produccion/crear_corte.html', {'form': form, 'detalle_formset': detalle_formset})


# En produccion/views.py
def lista_cortes(request):
    # Ordenamos por el número de reporte, del más alto al más bajo
    cortes = CorteDeBobina.objects.all().order_by('-numero_reporte')
    return render(request, 'produccion/lista_cortes.html', {'cortes': cortes})

# Agrega esta nueva función
def detalle_corte(request, corte_id):
    corte = get_object_or_404(CorteDeBobina, pk=corte_id)
    # También obtenemos los detalles (las bobinas) asociados a este reporte
    detalles = CorteDeBobinaDetalle.objects.filter(corte_de_bobina=corte)

    contexto = {
        'corte': corte,
        'detalles': detalles
    }
    return render(request, 'produccion/detalle_corte.html', contexto) 

# En produccion/views.py

# En produccion/views.py

def editar_corte(request, corte_id):
    # Buscamos el reporte de corte que se va a editar
    corte = get_object_or_404(CorteDeBobina, pk=corte_id)
    # Preparamos el formset para los detalles, SIN formularios extra
    DetalleFormSet = modelformset_factory(
        CorteDeBobinaDetalle, 
        form=CorteDeBobinaDetalleForm, 
        extra=0, 
        can_delete=True
    )

    if request.method == 'POST':
        # Si el usuario envía el formulario, procesamos los datos
        form = CorteDeBobinaForm(request.POST, instance=corte)
        detalle_formset = DetalleFormSet(request.POST, queryset=CorteDeBobinaDetalle.objects.filter(corte_de_bobina=corte))

        if form.is_valid() and detalle_formset.is_valid():
            form.save()

            instances = detalle_formset.save(commit=False)
            for instance in instances:
                instance.corte_de_bobina = corte
                instance.save()
            detalle_formset.save() # Para procesar los objetos marcados para eliminar

            messages.success(request, f'¡Reporte de Corte N° {corte.numero_reporte} actualizado exitosamente!')
            return redirect('lista_cortes')
    else:
        # Si el usuario solo está cargando la página, mostramos los datos existentes
        form = CorteDeBobinaForm(instance=corte)
        detalle_formset = DetalleFormSet(queryset=CorteDeBobinaDetalle.objects.filter(corte_de_bobina=corte))

    contexto = {
        'form': form,
        'detalle_formset': detalle_formset
    }
    # Aseguramos que renderice la plantilla correcta
    return render(request, 'produccion/crear_corte.html', contexto)

# En produccion/views.py

def eliminar_corte(request, corte_id):
    corte = get_object_or_404(CorteDeBobina, pk=corte_id)
    if request.method == 'POST':
        corte.delete()
        return redirect('lista_cortes')
    return render(request, 'produccion/eliminar_corte.html', {'corte': corte})

# En produccion/views.py

# En produccion/views.py

# En produccion/views.py

def buscar_bobinas_api(request):
    query = request.GET.get('term', '').strip() # Limpiamos espacios del término de búsqueda

    # Anotamos un campo 'codigo_limpio' sin espacios y filtramos por él
    bobinas = Producto.objects.using('rq').annotate(
        codigo_limpio=Trim('codigo')
    ).filter(
        Q(codigo_limpio__icontains=query) | Q(nombre__icontains=query),
        idsucursal=10,
        nombre3='BOBINA'
    ).order_by('codigo')[:15]

    resultados = []
    for bobina in bobinas:
        resultados.append({
            'id': bobina.codigo,
            'text': f"{bobina.codigo} | {bobina.nombre}",
            'existencia': bobina.cantidad
        })
    return JsonResponse(resultados, safe=False)

def buscar_papel_api(request):
    query = request.GET.get('term', '').strip() # Limpiamos espacios del término de búsqueda

    # Misma lógica robusta para el papel
    papeles = Producto.objects.using('rq').annotate(
        codigo_limpio=Trim('codigo')
    ).filter(
        Q(codigo_limpio__icontains=query) | Q(nombre__icontains=query),
        idsucursal=10,
        nombre3='PAPEL'
    ).order_by('nombre')[:15]

    resultados = []
    for papel in papeles:
        resultados.append({
            'id': papel.codigo,
            'text': f"{papel.codigo} | {papel.nombre}",
            'existencia': papel.cantidad
        })
    return JsonResponse(resultados, safe=False)

#30082025
# def lista_productos(request):
#     """
#     Muestra una lista de todos los productos de la sucursal 10.
#     El Manager personalizado que definimos en models.py se encarga del filtro.
#     """
#     productos = Producto.objects.all()
#     return render(request, 'produccion/producto_lista.html', {'productos': productos})
#31082025
# En produccion/views.py

def lista_productos(request):
    """
    Muestra una lista de productos, permitiendo filtrar por el campo 'nombre3'.
    """
    # 1. Obtener el valor del filtro desde la URL. 
    #    Ej: /productos/?filtro_tipo=BOBINA
    filtro_seleccionado = request.GET.get('filtro_tipo', '')

    # 2. Obtener la lista única de todos los tipos de producto (nombre3) para el dropdown
    tipos_productos = Producto.objects.order_by('nombre3').values_list('nombre3', flat=True).distinct()

    # 3. Empezar con todos los productos
    productos = Producto.objects.all()

    # 4. Si se seleccionó un filtro válido, aplicar el filtro a la consulta
    if filtro_seleccionado and filtro_seleccionado != "":
        productos = productos.filter(nombre3=filtro_seleccionado)

    contexto = {
        'productos': productos,
        'tipos_productos': tipos_productos, # <-- Pasamos la lista de tipos al template
        'filtro_seleccionado': filtro_seleccionado # <-- Pasamos el filtro actual para "recordarlo"
    }
    return render(request, 'produccion/producto_lista.html', contexto)


def crear_producto(request):
    """
    Crea un nuevo producto en la sucursal 10.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Guardamos el objeto en memoria sin enviarlo a la BD todavía
            producto = form.save(commit=False)
            
            # Asignamos los valores por defecto que no están en el formulario
            producto.idsucursal = 10
            producto.cantidad = 0
            
            # Ahora sí, guardamos el nuevo producto en la base de datos
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    
    # Pasamos un 'form' vacío para un producto nuevo
    return render(request, 'produccion/producto_form.html', {'form': form})

def editar_producto(request, pk):
    """
    Edita un producto existente de la sucursal 10.
    La llave primaria 'pk' ahora corresponde al campo 'orden'.
    """
    # get_object_or_404 usará el manager y solo encontrará productos de la sucursal 10
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        # Pasamos la instancia del producto para pre-llenar el formulario
        form = ProductoForm(instance=producto)
        
    return render(request, 'produccion/producto_form.html', {'form': form})

def verificar_producto_api(request):
    """
    API para verificar si un producto ya existe por código o nombre en la sucursal 10.
    """
    codigo = request.GET.get('codigo')
    nombre = request.GET.get('nombre')
    
    # La consulta ya está filtrada por idsucursal=10 gracias al manager.
    producto_existente = Producto.objects.filter(Q(codigo__iexact=codigo) | Q(nombre__iexact=nombre)).first()

    if producto_existente:
        data = {
            'existe': True,
            'id': producto_existente.pk, # El pk es el campo 'orden'
            'codigo': producto_existente.codigo,
            'nombre': producto_existente.nombre,
            'tipo': producto_existente.nombre3 # El tipo ahora es 'nombre3'
        }
    else:
        data = {'existe': False}
    
    return JsonResponse(data)

#31082025
# Al final de produccion/views.py

def buscar_productos_api(request):
    """
    API para buscar CUALQUIER producto por código o nombre.
    Devuelve resultados en el formato que espera la librería Select2.
    """
    # Obtenemos el término de búsqueda que envía el JavaScript de Select2
    query = request.GET.get('term', '').strip()

    # Si no hay término de búsqueda, devolvemos una lista vacía
    if not query:
        return JsonResponse({'results': []})

    # Buscamos productos cuyo código O nombre contengan el texto buscado
    # Usamos el manager 'objects' que ya filtra por sucursal 10
    productos_encontrados = Producto.objects.filter(
        Q(codigo__icontains=query) | Q(nombre__icontains=query)
    ).order_by('nombre')[:20] # Limitamos a 20 resultados por rendimiento

    # Formateamos los resultados como lo necesita Select2
    resultados = []
    for producto in productos_encontrados:
        resultados.append({
            'id': producto.codigo,  # El valor que se enviará en el formulario
            'text': f"{producto.codigo} | {producto.nombre}" # El texto que verá el usuario
        })

    return JsonResponse({'results': resultados})

#07092025
# --- AÑADE ESTA NUEVA API AL FINAL DEL ARCHIVO ---
def get_producto_detalle_api(request):
    """
    API que devuelve los detalles (como la cantidad) de un producto específico.
    """
    codigo_producto = request.GET.get('codigo')
    data = {'existe': False}
    try:
        # Usamos .get() que es estricto y asegura que solo haya un resultado
        producto = Producto.objects.using('rq').get(codigo=codigo_producto)
        data = {
            'existe': True,
            'cantidad': producto.cantidad,
            'nombre': producto.nombre
        }
    except Producto.DoesNotExist:
        # El producto no fue encontrado, data ya está como {'existe': False}
        pass
    
    return JsonResponse(data)


# 07092025--- AÑADE ESTA VISTA PRINCIPAL AL FINAL DEL ARCHIVO ---
# Usamos transaction.atomic para asegurar que ambas operaciones (Producto y Kardex)
# se completen exitosamente. Si una falla, la otra se revierte.
# --- REEMPLAZA TU VISTA 'ingreso_producto' CON ESTA VERSIÓN MEJORADA ---
@transaction.atomic(using='rq')
def ingreso_producto(request):
    if request.method == 'POST':
        # --- LÓGICA PARA GUARDAR LOS DATOS ---
        codigo = request.POST.get('producto_codigo')
        cantidad_ingresada_str = request.POST.get('cantidad', '0')
        descripcion = request.POST.get('descripcion')
        fecha_ingreso_str = request.POST.get('fecha') # <-- 1. Obtenemos la fecha del formulario

        if not all([codigo, cantidad_ingresada_str, descripcion, fecha_ingreso_str]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('ingreso_producto')

        try:
            cantidad_ingresada = decimal.Decimal(cantidad_ingresada_str)
            if cantidad_ingresada <= 0:
                messages.error(request, 'La cantidad a ingresar debe ser un número positivo.')
                return redirect('ingreso_producto')

            producto = Producto.objects.using('rq').select_for_update().get(codigo=codigo)
            nuevo_stock = producto.cantidad + cantidad_ingresada
            producto.cantidad = nuevo_stock
            producto.save()

            Kardex.objects.using('rq').create(
                producto=producto,
                codigo=producto.codigo,
                fecha=fecha_ingreso_str, # <-- 2. Usamos la fecha del formulario al guardar
                documento='INGRESO MANUAL',
                descripcion=descripcion,
                entrada=cantidad_ingresada,
                salida=0,
                saldo=nuevo_stock,
                idsucursal=10
            )

            messages.success(request, f'¡Ingreso de {cantidad_ingresada} para "{producto.nombre}" guardado exitosamente!')
            return redirect('lista_productos')

        except Producto.DoesNotExist:
            messages.error(request, 'Error: El producto seleccionado ya no existe.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al guardar: {e}')

        return redirect('ingreso_producto')

    # --- LÓGICA PARA MOSTRAR LA PÁGINA VACÍA ---
    contexto = {
        'today_date': date.today().strftime('%Y-%m-%d') # <-- 3. Pasamos la fecha de hoy a la plantilla
    }
    return render(request, 'produccion/ingreso_producto.html', contexto)

#07092025
# --- AÑADE ESTA NUEVA FUNCIÓN API AL FINAL DEL ARCHIVO ---
def get_siguiente_numero_api(request):
    """
    API que calcula el siguiente número correlativo para un tipo de documento específico.
    """
    tipo_documento = request.GET.get('tipo_documento')
    if not tipo_documento:
        return JsonResponse({'error': 'Tipo de documento no proporcionado'}, status=400)

    try:
        # Buscamos en el Kardex el número más alto para ese tipo de documento
        ultimo_numero = Kardex.objects.using('rq').filter(
            documento__startswith=f'{tipo_documento} N°'
        ).aggregate(max_num=Max('numero'))['max_num'] or 0
        siguiente_numero = ultimo_numero + 1
        return JsonResponse({'siguiente_numero': siguiente_numero})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- REEMPLAZA TU VISTA 'ingreso_producto' CON ESTA VERSIÓN ---
@transaction.atomic(using='rq')
def ingreso_producto(request):
    if request.method == 'POST':
        # --- LÓGICA PARA GUARDAR LOS DATOS ---
        codigo = request.POST.get('producto_codigo')
        cantidad_ingresada_str = request.POST.get('cantidad', '0')
        descripcion = request.POST.get('descripcion')
        fecha_ingreso_str = request.POST.get('fecha')
        tipo_documento = request.POST.get('tipo_documento')
        numero_referencia = request.POST.get('numero_referencia')

        try:
            cantidad_ingresada = decimal.Decimal(cantidad_ingresada_str)
            if cantidad_ingresada <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")

            producto = Producto.objects.using('rq').select_for_update().get(codigo=codigo)
            nuevo_stock = producto.cantidad + cantidad_ingresada
            producto.cantidad = nuevo_stock
            producto.save()

            Kardex.objects.using('rq').create(
                producto=producto,
                codigo=producto.codigo,
                fecha=fecha_ingreso_str,
                documento=f'{tipo_documento} N° {numero_referencia}',
                descripcion=descripcion,
                entrada=cantidad_ingresada,
                salida=0,
                saldo=nuevo_stock,
                idsucursal=10,
                numero=numero_referencia
            )

            messages.success(request, f'¡{tipo_documento} N° {numero_referencia} guardado exitosamente!')
            return redirect('lista_productos')

        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al guardar: {e}')
            return redirect('ingreso_producto')

    # --- LÓGICA PARA MOSTRAR LA PÁGINA (GET) ---
    contexto = {
        'today_date': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'produccion/ingreso_producto.html', contexto)

# --- AÑADE ESTA NUEVA VISTA AL FINAL DEL ARCHIVO ---
def reporte_movimientos(request):
    # Obtenemos las fechas del formulario. Si no existen, usamos valores vacíos.
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    # Empezamos con una consulta vacía
    movimientos = Kardex.objects.none()

    # Solo ejecutamos la búsqueda si el usuario ha enviado al menos una fecha
    if fecha_desde or fecha_hasta:
        # Usamos select_related para traer también la información del producto
        # y evitar consultas extra a la base de datos.
        query = Kardex.objects.using('rq').select_related('producto')

        if fecha_desde:
            query = query.filter(fecha__date__gte=fecha_desde)
        
        if fecha_hasta:
            query = query.filter(fecha__date__lte=fecha_hasta)
        
        # Ordenamos los resultados por fecha, del más reciente al más antiguo
        movimientos = query.order_by('-fecha')

    contexto = {
        'movimientos': movimientos,
        'fecha_desde_valor': fecha_desde,
        'fecha_hasta_valor': fecha_hasta,
    }
    return render(request, 'produccion/reporte_movimientos.html', contexto)

def lista_movimientos(request):
    """
    Muestra una lista de documentos de movimiento, permitiendo filtrar por tipo.
    Ahora solo considera los tipos de movimiento manuales.
    """
    tipo_seleccionado = request.GET.get('tipo', '')

    # 1. Definimos los tipos de documento que nos interesan para esta consulta.
    tipos_manuales = ['INGRESO', 'AJUSTE', 'DEVOLUCION']

    # 2. La consulta base ahora solo traerá movimientos de la sucursal 10.
    movimientos_base = Kardex.objects.using('rq').filter(idsucursal=10)
    
    # --- INICIO DE LA CORRECCIÓN ---
    # 3. Asignamos la lista de tipos manuales a la variable que usará el contexto.
    tipos_documento_para_filtro = tipos_manuales
    # --- FIN DE LA CORRECCIÓN ---

    # Aplicamos el filtro si el usuario seleccionó un tipo de documento
    if tipo_seleccionado:
        movimientos_base = movimientos_base.filter(documento__startswith=f"{tipo_seleccionado} N°")

    # Agrupamos para obtener la lista de documentos únicos para la tabla
    movimientos_unicos_qs = movimientos_base.values(
        'documento', 'numero', 'fecha'
    ).distinct().order_by('-fecha', '-numero')

    # Procesamos los datos para la plantilla
    movimientos_procesados = []
    for mov in movimientos_unicos_qs:
        if not mov['documento'] or mov['numero'] is None:
            continue
        partes_documento = mov['documento'].split(' N° ')
        if len(partes_documento) > 0:
            tipo_doc = partes_documento[0]
            try:
                numero_limpio = int(mov['numero'])
                movimientos_procesados.append({
                    'tipo_documento': tipo_doc,
                    'numero': numero_limpio,
                    'fecha': mov['fecha']
                })
            except (ValueError, TypeError):
                continue

    contexto = {
        'movimientos': movimientos_procesados,
        'tipos_documento': tipos_documento_para_filtro, # Usamos la variable correcta
        'tipo_seleccionado': tipo_seleccionado
    }
    return render(request, 'produccion/lista_movimientos.html', contexto)

# def lista_movimientos(request):
#     """
#     Muestra una lista de todos los documentos de movimiento de inventario,
#     agrupados por su tipo y número de referencia.
#     """
#     # --- INICIO DE LA CORRECCIÓN ---
#     # Añadimos el filtro para mostrar únicamente los movimientos de la sucursal 10
#     movimientos_unicos_qs = Kardex.objects.using('rq').filter(idsucursal=10 and Documento='INGRESO').values(
#         'documento', 
#         'numero',
#         'fecha'
#     ).distinct().order_by('-fecha', '-numero')
#     # --- FIN DE LA CORRECCIÓN ---

#     movimientos_procesados = []
#     for mov in movimientos_unicos_qs:
#         # Ignoramos registros que no tengan un documento o número válido
#         if not mov['documento'] or mov['numero'] is None:
#             continue

#         partes_documento = mov['documento'].split(' N° ')
#         if len(partes_documento) > 0:
#             tipo_doc = partes_documento[0]

#             # --- INICIO DE LA CORRECCIÓN ---
#             # Nos aseguramos de que el número sea un entero limpio,
#             # eliminando cualquier espacio y convirtiéndolo a número.
#             try:
#                 numero_limpio = int(mov['numero'])
#             except (ValueError, TypeError):
#                 # Si por alguna razón el número no es válido, ignoramos este registro para evitar que la página se caiga.
#                 continue
#             # --- FIN DE LA CORRECCIÓN ---

#             movimientos_procesados.append({
#                 'tipo_documento': tipo_doc,
#                 'numero': numero_limpio, # <-- Usamos el número ya limpio
#                 'fecha': mov['fecha']
#             })

#     contexto = {
#         'movimientos': movimientos_procesados
#     }
#     return render(request, 'produccion/lista_movimientos.html', contexto)

def detalle_movimiento(request, tipo_documento, numero):
    """
    Muestra el detalle de un movimiento de inventario específico.
    """
    # --- INICIO DE LA CORRECCIÓN ---
    # La URL ahora usa un formato "slug" (ej: ajuste-de-inventario).
    # Lo revertimos a su forma original reemplazando guiones por espacios.
    tipo_documento_real = tipo_documento.replace('-', ' ')
    # --- FIN DE LA CORRECCIÓN ---
    
    documento_completo = f"{tipo_documento_real} N° {numero}"

    detalles_movimiento = Kardex.objects.using('rq').select_related('producto').filter(
        documento=documento_completo
    ).order_by('producto__nombre')

    contexto = {
        'encabezado': detalles_movimiento.first(), 
        'detalles': detalles_movimiento
    }
    return render(request, 'produccion/detalle_movimiento.html', contexto)
# def detalle_movimiento(request, tipo_documento, numero):
#     """
#     Muestra el detalle de un movimiento de inventario específico,
#     listando todos los productos que se incluyeron en esa transacción.
#     """
#     # Reemplazamos los guiones bajos que pueda traer la URL por espacios
#     tipo_documento_real = tipo_documento.replace('_', ' ')
    
#     # Construimos el nombre completo del documento para la búsqueda
#     documento_completo = f"{tipo_documento_real} N° {numero}"

#     # Buscamos todos los registros del kardex que pertenecen a este documento
#     detalles_movimiento = Kardex.objects.using('rq').select_related('producto').filter(
#         documento=documento_completo
#     ).order_by('producto__nombre')

#     contexto = {
#         # Pasamos solo el primer resultado para los datos generales (fecha, etc.)
#         'encabezado': detalles_movimiento.first(), 
#         # Pasamos todos los resultados para la tabla de detalles
#         'detalles': detalles_movimiento
#     }
#     return render(request, 'produccion/detalle_movimiento.html', contexto)