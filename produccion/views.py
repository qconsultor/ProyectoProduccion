# Al principio de produccion/views.py
from datetime import date
from django.db.models import Q
from django.db.models.functions import Trim
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory,modelformset_factory # <-- ¡AÑADE ESTA LÍNEA!
from django.contrib import messages
# Al principio de produccion/views.py
from .models import (
    OrdenProduccion, RequisicionEncabezado, ControlProceso, CorteDeBobina, CorteDeBobinaDetalle, 
    ReporteDiarioProductoTerminado, NotaIngresoProductoTerminado, 
    Producto, Kardex
)
#from .forms import OrdenProduccionForm, RequisicionForm
from .forms import OrdenProduccionForm, RequisicionForm, ControlProcesoForm , ReporteDiarioForm , NotaIngresoForm, CorteDeBobinaForm, CorteDeBobinaDetalleForm, CorteDeBobinaDetalleFormEditar

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

def detalle_control(request, control_id):
    control = get_object_or_404(ControlProceso, pk=control_id)
    contexto = {'control': control}
    return render(request, 'produccion/detalle_control.html', contexto)

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

def editar_control(request, control_id):
    # Obtenemos el objeto principal (el encabezado)
    control = get_object_or_404(ControlProceso, pk=control_id)

    # Creamos una "fábrica" de formsets para los detalles.
    # Le decimos que trabaje con el modelo padre e hijo, y que muestre un formulario extra.
    ControlProcesoDetalleFormSet = inlineformset_factory(
        ControlProceso, 
        ControlProcesoDetalle, 
        fields=('fecha', 'turno', 'compaginado', 'doblado_libro', 'doblado_portada', 'engrapado', 'pegado', 'refilado', 'empacado', 'unidades'),
        extra=1, # Muestra un formulario en blanco para añadir un nuevo detalle
        can_delete=True # Permite borrar detalles existentes
    )

    if request.method == 'POST':
        # Si el usuario envía datos, llenamos el formulario principal Y el formset
        form = ControlProcesoForm(request.POST, instance=control)
        formset = ControlProcesoDetalleFormSet(request.POST, instance=control)

        # Verificamos que AMBOS sean válidos
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('detalle_control', control_id=control.id) # Volvemos al detalle para ver los cambios
    else:
        # Si el usuario solo visita la página, mostramos el formulario y el formset llenos con los datos existentes
        form = ControlProcesoForm(instance=control)
        formset = ControlProcesoDetalleFormSet(instance=control)

    contexto = {
        'form': form,
        'formset': formset, # Pasamos también el formset a la plantilla
        'control': control,
    }
    return render(request, 'produccion/crear_control.html', contexto)

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

    

def reporte_kardex(request):
    codigo_buscado = request.GET.get('codigo_producto', '')
    # --- NUEVO: Obtenemos las fechas del formulario ---
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    movimientos = None

    if codigo_buscado:
        # Empezamos filtrando por el código del producto
        movimientos = Kardex.objects.using('rq').filter(codigo=codigo_buscado)

        # --- NUEVO: Si hay fechas, añadimos más filtros a la consulta ---
        if fecha_desde:
            # __date__gte = la FECHA del campo sea "mayor o igual que"
            movimientos = movimientos.filter(fecha__date__gte=fecha_desde)

        if fecha_hasta:
            # __date__lte = la FECHA del campo sea "menor o igual que"
            movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)

        # Ordenamos el resultado final
        movimientos = movimientos.order_by('fecha')

    contexto = {
        'movimientos': movimientos,
        'codigo_buscado': codigo_buscado,
        # --- NUEVO: Devolvemos las fechas a la plantilla para que las "recuerde" ---
        'fecha_desde_valor': fecha_desde,
        'fecha_hasta_valor': fecha_hasta,
    }
    return render(request, 'produccion/reporte_kardex.html', contexto)
def reporte_kardex_imprimir(request):
    codigo_buscado = request.GET.get('codigo_producto', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    movimientos = None
    producto = None

    if codigo_buscado:
        # Aquí filtramos los movimientos
        movimientos = Kardex.objects.using('rq').filter(codigo=codigo_buscado, idsucursal=10)
        
        # Y aquí corregimos la búsqueda del producto
        try:
            # --- LÍNEA CORREGIDA ---
            producto = Producto.objects.using('rq').get(codigo=codigo_buscado, idsucursal=10)
        except (Producto.DoesNotExist, Producto.MultipleObjectsReturned):
            # Si no se encuentra o hay duplicados (aunque no debería pasar ya), lo manejamos
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

