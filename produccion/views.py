# Al principio de produccion/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
# Al principio de produccion/views.py
from .models import (
    OrdenProduccion, RequisicionEncabezado, ControlProceso, CorteDeBobina, 
    ReporteDiarioProductoTerminado, NotaIngresoProductoTerminado, 
    Producto, Kardex
)
#from .forms import OrdenProduccionForm, RequisicionForm
from .forms import OrdenProduccionForm, RequisicionForm, ControlProcesoForm , ReporteDiarioForm , NotaIngresoForm

# Create your views here. ORDENES
def lista_ordenes(request):
    # Empezamos con todas las órdenes
    queryset = OrdenProduccion.objects.all()

    # Obtenemos los valores de los filtros de la URL (son peticiones GET)
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    # Si el usuario proporcionó una fecha 'desde', filtramos el queryset
    if fecha_desde:
        queryset = queryset.filter(fecha__gte=fecha_desde)

    # Si el usuario proporcionó una fecha 'hasta', filtramos el queryset
    if fecha_hasta:
        queryset = queryset.filter(fecha__lte=fecha_hasta)

    contexto = {
        'ordenes': queryset,
        # Pasamos los valores de los filtros para que se queden en los campos
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